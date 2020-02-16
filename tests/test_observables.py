from unittest import TestCase
import os
import tempfile
import random

import pyeti

def _random_string():
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(16))

def _random_domain(tld='com'):
    return "{}.{}".format(_random_string(), tld)


class TestAPI(TestCase):
    url = 'http://localhost:5000/api'

    def setUp(self):
        self.api = pyeti.YetiApi(self.url)

    def test_observable_add(self):
        """Adds an observable with tags and tests for that value and tags match."""
        domain = _random_domain()
        info = self.api.observable_add(domain, ['asd'])
        self.assertEqual(info['value'], domain)
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd'])

    def test_observable_delete(self):
        domain = _random_domain()
        info = self.api.observable_add(domain)
        details = self.api.observable_details(info["id"])
        self.assertEqual(details['value'], domain)
        result = self.api.observable_delete(info['id'])
        self.assertEqual(result, {'status': 'deleted', 'id': info['id']})
        details = self.api.observable_details(domain)
        self.assertIs(details, None)

    def test_observable_details(self):
        """Adds an observable and then fetches its details."""
        domain = _random_domain()
        info = self.api.observable_add(domain)
        info = self.api.observable_details(info['id'])
        self.assertEqual(info['value'], domain)

    def test_observable_change(self):
        """Adds an observable and tries to add a tag."""
        domain = _random_domain()
        info = self.api.observable_add(domain, ['asd'])
        info = self.api.observable_change(info['id'], tags=['dsa'])
        tags = [t['name'] for t in info['tags']]
        self.assertEqual(tags, ['asd', 'dsa'])

    def test_observable_by_tag(self):
        domain = _random_domain()
        tag = _random_string()
        self.api.observable_add(domain, [tag])
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
        result = self.api.observable_add('hxxp://test.com/')
        self.assertEqual(result['value'], 'http://test.com/')

        result = self.api.observable_add('hxxps://test[.]com/')
        self.assertEqual(result['value'], 'https://test.com/')

        result = self.api.observable_add('test[.]com')
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


if __name__ == '__main__':
    TestCase.main()
