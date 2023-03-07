from unittest import TestCase
import os
import tempfile
import random
from configparser import ConfigParser
import unittest
import pyeti

def _random_string():
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))

def _random_domain(tld='com'):
    return "{}.{}".format(_random_string(), tld)


class TestAPI(TestCase):
    """Tests for Yeti API."""
    def setUp(self):
            config = ConfigParser()
            config.read("pyeti.conf")
            url = config.get('yeti', 'url')
            api_key = config.get('yeti', 'api_key')
            self.api = pyeti.YetiApi(url=url, api_key= api_key)

    def test_add_ip(self):
        """Adds an IP with tags and tests for that value and tags match."""
        ip = '1.1.1.1'
        info = self.api.add_ipadress(ip, tags=['asd'])
        self.assertEqual(info['value'], ip)
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd'])

    def test_add_macaddress(self):
        """Adds an MAC with tags and tests for that value and tags match."""
        mac = '00:00:00:00:00:00'
        info = self.api.add_macaddress(mac, tags=['asd'])
        self.assertEqual(info['value'], mac)
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd'])

    def test_add_email(self):
        """Adds an email with tags and tests for that value and tags match."""
        email = 'test@test.com'
        info = self.api.add_email(email, tags=['asd'])
        self.assertEqual(info['value'], email)
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd'])

    def test_add_url(self):
        """Adds an url with tags and tests for that value and tags match."""
        url = 'http://test.com/'
        info = self.api.add_url(url, tags=['asd'])
        self.assertEqual(info['value'], url)
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd'])

    def test_add_text(self):
        """Adds an text with tags and tests for that value and tags match."""
        text = 'test'
        info = self.api.add_text(text, tags=['asd'])
        self.assertEqual(info['value'], text)
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd'])
    
    def test_add_path(self):
        """Adds an path with tags and tests for that value and tags match."""
        path = 'C:\\test\\'
        info = self.api.add_path(path, tags=['asd'])
        self.assertEqual(info['value'], path)
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd'])
    
    def test_add_hash(self):
        """Adds an hash with tags and tests for that value and tags match."""
        hash = '08be2c7239acb9557454088bba877a245c8ef9b0e9eb389c65a98e1c752c5709'
        info = self.api.add_hash(hash, tags=['asd'])
        self.assertEqual(info['value'], hash)
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd'])
    
    def test_add_hostname(self):
        """Adds a hostname with tags and tests for that value and tags match."""
        hostname = 'test123.com'
        info = self.api.add_hostname(hostname, tags=['asd'])
        self.assertEqual(info['value'], hostname)
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd'])
    
    def test_add_asn(self):
        """Adds an asn with tags and tests for that value and tags match."""
        asn = '123'
        info = self.api.add_asn(asn, tags=['asd'])
        self.assertEqual(info['value'], asn)
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd'])
    
    def test_add_bitcoin(self):
        """Adds a bitcoin with tags and tests for that value and tags match."""
        bitcoin = '115p7UMMngoj1pMvkpHijcRdfJNXj6LrLn'
        info = self.api.add_bitcoin(bitcoin, tags=['asd'])
        self.assertEqual(info['value'], bitcoin)
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd'])
    
    def test_observable_delete(self):
        domain = _random_domain()
        info = self.api.add_hostname(domain)
        details = self.api.observable_details(info["id"])
        self.assertEqual(details['value'], domain)
        result = self.api.observable_delete(info['id'])
        self.assertEqual(result, {'status': 'deleted', 'id': info['id']})
        details = self.api.observable_details(domain)
        self.assertIs(details, None)

    def test_observable_details(self):
        """Adds an observable and then fetches its details."""
        domain = _random_domain()
        info = self.api.add_hostname(domain)
        info = self.api.observable_details(info['id'])
        self.assertEqual(info['value'], domain)
    
    def test_observable_change(self):
        """Adds an observable and tries to add a tag."""
        domain = _random_domain()
        info = self.api.add_hostname(domain, ['asd'])
        info = self.api.observable_change(info['id'], tags=['dsa'])
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd', 'dsa'])
    
    def test_observable_by_tag(self):
        domain = _random_domain()
        tag = _random_string()
        self.api.add_hostname(domain, [tag])
        results = self.api.observable_search(tags=tag)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['value'], domain)
        tags = [t['name'] for t in results[0]['tags']]
        self.assertIn(tag, tags)

    def test_bulk_observable_add(self):
        """Adds an observables in bulk."""
        observables = ["{}{}.com".format(_random_domain(), i) for i in range(20)]
        info = self.api.observable_bulk_add(observables, ['bulk'])
        self.assertEqual(len(info), 20)

    def test_bulk_observable_refang_add(self):
        """Adds defanged observables in bulk."""
        observables = ["hxxp://{}{}.com".format(_random_domain(), i) for i in range(20)]
        info = self.api.observable_bulk_add(observables, ['bulk'])
        self.assertEqual(len(info), 20)
        for url in info:
            self.assertIn('http://', url['value'])

    def test_observable_refang(self):
        """Adds a defanged observable and tests that it is refanged."""
        result = self.api.add_url('hxxp://test.com/')
        self.assertEqual(result['value'], 'http://test.com/')
        result = self.api.add_url('hxxps://test[.]com/')
        self.assertEqual(result['value'], 'https://test.com/')
        result = self.api.add_hostname('test[.]com')
        self.assertEqual(result['value'], 'test.com')

    def test_observable_url_normalize(self):
        """Adds a valid URL is normalized."""
        result = self.api.observable_add('http://test.com')
        self.assertEqual(result['value'], 'http://test.com/')
        result = self.api.observable_add('https://test.com/something/../asd')
        self.assertEqual(result['value'], 'https://test.com/asd')
    def test_observable_file_add(self):
        """Creates a temporary file and attempts to upload it to Yeti."""
        with tempfile.NamedTemporaryFile('wb', delete=False) as f:
            f.write(b"content")
            filename = f.name
        fileinfo = self.api.observable_file_add(filename, ['file_tag'])
        os.remove(filename)
        # SHA256 of "content"
        expected_filename = "FILE:ed7002b439e9ac845f22357d822bac1444730fbdb6016d3ec9432297b9ec9f73"
        self.assertEqual(fileinfo[0]['value'], expected_filename)
        tags = [t['name'] for t in fileinfo[0]['tags']]
        self.assertEqual(tags, ['file_tag'])
    def test_file_download_by_id(self):
        with tempfile.NamedTemporaryFile('wb', delete=False) as f:
            f.write(b"content")
            filename = f.name
        fileinfo = self.api.observable_file_add(filename, ['file_tag'])[0]
        os.remove(filename)
        content_by_id = self.api.observable_file_contents(objectid=fileinfo['id'])
        self.assertEqual(content_by_id, b"content")
    def test_file_download_by_hash(self):
        with tempfile.NamedTemporaryFile('wb', delete=False) as f:
            f.write(b"content")
            filename = f.name
        self.api.observable_file_add(filename, ['file_tag'])
        os.remove(filename)
        # SHA256 of "content"
        filehash = "ed7002b439e9ac845f22357d822bac1444730fbdb6016d3ec9432297b9ec9f73"
        content_by_hash = self.api.observable_file_contents(filehash=filehash)
        self.assertEqual(content_by_hash, b"content")
    def test_analysis_match(self):
        """Calls the match endpoint with a known and an unknown domain."""
        self.api.observable_add('test.com')
        results = self.api.analysis_match(['test.com', 'unknown.com'])
        known = [o['value'] for o in results['known']]
        self.assertIn('test.com', known)
        self.assertIn('unknown.com', results['unknown'])
    def test_observable_search(self):
        """Adds a semi-random domain name and tries searching for it."""
        domain = _random_domain()
        self.api.observable_add("search-"+domain)
        result = self.api.observable_search(regex=True, value=domain)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['value'], "search-"+domain)


    def test_force_type(self):
        asn = self.api.observable_add(value="1234",type_obs="AutonomousSystem")
        if not asn:
            self.assertIsNotNone(asn)
        
        asn_added = self.api.observable_search(value="1234")
        if not asn_added:
            self.assertIsNotNone(asn_added)

        self.assertEqual(asn_added[0]["value"], "1234")

if __name__ == "__main__":
    unittest.main()
