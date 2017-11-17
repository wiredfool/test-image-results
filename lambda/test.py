import service

import unittest
from PIL import Image
import requests

class TestService(unittest.TestCase):

    SRC = Image.open('images/hopper.png')
    
    def setup(self):
        with open('images/hopper.png', 'rb') as f:
            service.set_fromBytes('test/hopper.png', f.read())
    
    def test_diffcore(self):

        d = service.diff_core(self.SRC,self.SRC)
        # identical
        self.assertEquals(d.getpixel((0,0)), (0,0,0)) 

        # different mode, but no crashing
        d = service.diff_core(self.SRC.convert('P'), self.SRC) 
        d = service.diff_core(self.SRC.convert('RGB'), self.SRC.convert('RGBA'))
        d = service.diff_core(self.SRC.convert('L'), self.SRC)

    def test_saveaspng(self):
        service.save_asPng('test/save.png', self.SRC)
        img = service.get_asImage('test/save.png')

        self.assertEqual(img.size, self.SRC.size)
        self.assertEqual(img.mode, self.SRC.mode)

    def test_perform_diff(self):
        service.save_asPng('test/target', self.SRC)
        service.save_asPng('test/result', self.SRC.convert('P'))

        service.perform_diff('test')

        d = service.get_asImage('test/diff.png')
        self.assertEqual(d.mode, self.SRC.mode)
        self.assertEqual(d.size, self.SRC.size)

        self.assert_(service.diff_exists('test'))
        
    def test_diff_exists(self):
        self.assertFalse(service.diff_exists('does_not_exist'))
        
    def test_signed_urls(self):
        urls = service.signed_urls('test')
        for url in urls.values():
            r = requests.get(url)
            r.raise_for_status()

    def test_signed_upload_urls(self):
        # end to end test
        urls = service.signed_upload_urls('test_upload')

        with open('images/hopper.png', 'rb') as f:
            data = f.read()

        for url in urls.values():
            r = requests.post(url['url'], data=url['fields'], files={'file':data})
            r.raise_for_status()

        service.perform_diff('test_upload')

        urls = service.signed_urls('test_upload')
        for url in urls.values():
            requests.get(url).raise_for_status()
    

if __name__=='__main__':
    unittest.main()
