from __future__ import print_function

from test_image_results import client
import unittest
import requests
from PIL import Image

class TestClient(unittest.TestCase):

    SRC = Image.open('../lambda/images/hopper.png')

    def test_geturls(self):
        urls = client._geturls()
        self.assert_(urls['display'])
        self.assert_(urls['upload']['result']['url'])
        self.assert_(urls['upload']['target']['url'])

    def test_convert(self):
        stream = client._convert(self.SRC)
        self.assertEqual(stream[:4], b'\x89PNG')
    
    def test_upload(self):
        url = client.upload(self.SRC.convert('P'), self.SRC)
        self.assert_(url)
        r = requests.get(url)
        r.raise_for_status()
        self.assert_('https://' in r.text)

        print ("\n")
        print (url)

if __name__=='__main__':
     unittest.main()
