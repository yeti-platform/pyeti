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
    
    def test_path(self):
        path = 'C:\\test\\'
        tags = ['asd']
        info = self.client.add_path(path, tags=tags)
        self.assertEqual(info['value'], path)
    
    def test_asn(self):
        asn = 'AS123'
        tags = ['asd']
        info = self.client.add_asn(asn, tags=tags)
        self.assertEqual(info['value'], asn)
    
    def test_cidr(self):
        cidr = '1.1.1.1/8'
        tags = ['asd']
        info = self.client.add_cidr(cidr, tags=tags)
        self.assertEqual(info['value'], cidr)
    
    def test_certificate(self):
        certificate = 'cert_test'
        tags = ['asd']
        info = self.client.add_certificate(certificate, tags=tags)
        self.assertEqual(info['value'], certificate)

    def test_bitcoin_wallet(self):
        bitcoin_wallet = '115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn'
        tags = ['asd']
        info = self.client.add_bitcoin_wallet(bitcoin_wallet, tags=tags)
        self.assertEqual(info['value'], bitcoin_wallet)

    def test_macaddress(self):
        macaddress = '00:00:00:00:00:00'
        tags = ['asd']
        info = self.client.add_macaddress(macaddress, tags=tags)
        self.assertEqual(info['value'], macaddress)
    
    def test_command_line(self):
        command_line = 'cmd.exe /c calc.exe'
        tags = ['asd']
        info = self.client.add_command_line(command_line, tags=tags)
        self.assertEqual(info['value'], command_line)
    
    def test_registry_key(self):
        registry_key = 'HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
        tags = ['asd']
        info = self.client.add_registry_key(registry_key, tags=tags)
        self.assertEqual(info['value'], registry_key)
    
    def test_imphash(self):
        imphash = '08be2c7239acb9557454088bba877a245c8ef9b0e9eb389c65a98e1c752c5709'
        tags = ['asd']
        info = self.client.add_imphash(imphash, tags=tags)
        self.assertEqual(info['value'], imphash)
    
    def test_tlsh(self):
        tlsh = 'T123456789012345678901234567890123456789012345678901234567890123456789012'
        tags = ['asd']
        info = self.client.add_tlsh(tlsh, tags=tags)
        self.assertEqual(info['value'], tlsh)
    
    def test_ssdeep(self):
        ssdeep = '3:123456789012345678901234567890123:123456789012345678901234567890123'
        tags = ['asd']
        info = self.client.add_ssdeep(ssdeep, tags=tags)
        self.assertEqual(info['value'], ssdeep)
        
    def test_observable(self):
        value = 'test.com'
        observable_type = 'hostname'
        res = self.client.observable_search(value,observable_type)
         

if __name__ == '__main__':
    unittest.main()

