from __future__ import print_function

import urllib
import base64
import subprocess
import os
import boto3
import io
import time
import json

from PIL import Image, ImageChops


s3 = boto3.resource('s3')
client = boto3.client('s3')
BUCKET = os.environ.get('S3_BUCKET', 'pillow-test-image-results')

"""
flow:
   GET upload_urls() -> timestamped directory in s3, returns target/result pair 
         of structures, display url 
         returns JSON
   client posts images to the urls specified
   client prints display url in the logs

   web browser hits display url, gets page with target/result/diff urls in the html. 
"""
         
         
def get_asImage(path):
    f = io.BytesIO()
    s3.Object(BUCKET, path).download_fileobj(f)
    return Image.open(f)

def set_fromBytes(path, data):
    s3.Object(BUCKET, path).put(Body=data) 

def normalize_modes(result, target):
    if (result.mode != target.mode):
        result = result.convert(target.mode)
    return result

def save_asPng(path, img):
    out = io.BytesIO()
    img.save(out, format='PNG')
    set_fromBytes(path, out.getvalue())

def diff_core(result, target):
    result = normalize_modes(result, target)
    return ImageChops.difference(result, target)
    
def perform_diff(test_case):
    result = get_asImage("%s/result" % test_case)
    target = get_asImage("%s/target" % test_case)

    diff = diff_core(result, target)
    
    save_asPng("%s/diff.png" % test_case, diff)

def diff_exists(test_case):
    try:
        metadata = client.head_object(Bucket=BUCKET, Key="%s/diff.png" % test_case)
        return metadata['ContentLength'] and True
    except:
        return False
    
def signed_urls(test_case):
    def gen_one(stub):
        return client.generate_presigned_url('get_object', {'Bucket':BUCKET, 'Key':stub})
    return {
        'result': gen_one("%s/result" % test_case),
        'target':gen_one("%s/target" % test_case),
        'diff': gen_one("%s/diff.png" % test_case),
        }

def signed_upload_urls(test_case):
    def gen_one(stub):
        return client.generate_presigned_post(Bucket=BUCKET, Key=stub)
    return {
        'result': gen_one("%s/result" % test_case),
        'target':gen_one("%s/target" % test_case),
        }


def upload(*args):
    slug = time.time()
    body = {'display': '/show/%s/'%slug,
            'upload': signed_upload_urls(slug)
    }
    return {'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(body)
            }

def retrieve(test_case, *args):

    if not diff_exists(test_case):
        perform_diff(test_case)
    
    body = """
<html><title>ImageComparision</title>
<body>Test Result:<br>
<img src='%(result)s'><br>
Test Target:<br>
<img src='%(target)s'><br>
Test Difference:<br>
<img src='%(diff)s'><br>
</body></html>
""" % signed_urls(test_case)
                        
    return {'headers': {'Content-Type': 'text/html'},
            'body': body
            }


urls = {
    'upload': upload,
    'show': retrieve,
}

def lambda_handler(event, context):
    print ("Event: %s" % event)
    
    path_elements = event['path'].split('/')[1:]
    print ("PathElements: %s" % path_elements)
    
    handler = path_elements[0]

    return urls.get(handler)(*path_elements[1:])
