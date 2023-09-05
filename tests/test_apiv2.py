from unittest import TestCase
import os
import tempfile
import random
from configparser import ConfigParser
import unittest
import pyeti

class TestAPIv2(unittest.TestCase):

    def setUp(self) -> None:
        config = ConfigParser()
        config.read("yeti.conf")
        url = config.get('yeti', 'url')
        api_key = config.get('yeti', 'api_key')
        self.client = pyeti.YetiClient(api_key=api_key,base_url=url)
        
    def test_add_ip(self):

        ip = '1.1.1.1'
        tags = ['asd']
        info = self.client.add_ipadress(ip, tags=tags)
        self.assertEqual(info['value'], ip)
    
    def test_hostname(self):
        hostname = 'test.com'
        tags = ['asd']
        info = self.client.add_hostname(hostname, tags=tags)
        self.assertEqual(info['value'], hostname)
    
    def test_url(self):
        url = 'http://test.com'
        tags = ['asd']
        info = self.client.add_url(url, tags=tags)
        self.assertEqual(info['value'], url)
    
    def test_email(self):
        email = 'test@test.com'
        tags = ['asd']
        info = self.client.add_email(email, tags=tags)
        self.assertEqual(info['value'], email)
    
    def test_file(self):
        file = 'test.txt'
        tags = ['asd']
        info = self.client.add_file(file, tags=tags)
        self.assertEqual(info['value'], file)
    
    def test_observable(self):
        value = 'test.com'
        observable_type = 'hostname'
        res = self.client.observable_search(value,observable_type)
         

if __name__ == '__main__':
    unittest.main()

