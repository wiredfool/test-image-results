
import requests
import os
import io
import logging

API = 'https://fmuvehxed0.execute-api.us-east-2.amazonaws.com/prod'
API_KEY = os.environ.get('PILLOW_TEST_API_KEY', None)

# suppress requests logging info
logging.getLogger('requests').setLevel(logging.ERROR)

def _send_one(presigned_struct, img):
    requests.post(presigned_struct['url'],
                  data=presigned_struct['fields'],
                  files={'file':img}).raise_for_status()

def _convert(img):
    out = io.BytesIO()
    img.save(out, format='PNG')
    return out.getvalue()

def _geturls():
    req = requests.get(API+'/upload', headers={'x-api-key': API_KEY})
    req.raise_for_status()
    return req.json()

def upload(result, target):
    if not API_KEY: return

    urls = _geturls()

    _send_one(urls['upload']['result'], _convert(result))
    _send_one(urls['upload']['target'], _convert(target))

    return API + urls['display']
                        

