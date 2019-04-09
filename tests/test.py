from unittest import TestCase

import pyeti


class TestAPI(TestCase):
    url = 'http://localhost:5000'
    fake_host = False

    if fake_host:
        import SimpleHTTPServer
        import SocketServer
        PORT = 5000

        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

        httpd = SocketServer.TCPServer(("", PORT), Handler)

        print("serving at port", PORT)
        httpd.serve_forever()

    def test_have_class(self):
        try:
            self.test = pyeti.YetiApi()
        except NameError as e:
            pass  # fail appropriately here.
        except TypeError as e:
            pass  # fail appropriately here.

    def test_YetiApi_without_arg(self):
        with self.assertRaises(TypeError) as context:
            pyeti.YetiApi()
        self.assertFalse('This is broken' in str(context.exception))

    def test_YetiApi_with_url(self):
        try:
            self.test = pyeti.YetiApi('http://localhost:5000')
        except TypeError as e:
            pass  # fail appropriately here.

    def test_YetiApi_with_url_ignore_ssl(self):
        try:
            self.test = pyeti.YetiApi('http://localhost:5000', verify_ssl=False)
        except TypeError as e:
            pass  # fail appropriately here.

    def test_has_analysis_match(self):
        api = pyeti.YetiApi(self.url)
        with self.assertRaises(TypeError) as context:
            api.analysis_match()
        self.assertFalse('This is broken' in str(context.exception))

    def test_has_observable_search(self):
        api = pyeti.YetiApi(self.url)
        try:
            api.observable_search()
        except:
            pass

    def test_has_observable_details(self):
        api = pyeti.YetiApi(self.url)
        with self.assertRaises(TypeError) as context:
            api.observable_details()
        self.assertFalse('This is broken' in str(context.exception))

    def test_observable_add(self):
        api = pyeti.YetiApi(self.url)
        with self.assertRaises(TypeError) as context:
            api.observable_add()
        self.assertFalse('This is broken' in str(context.exception))

    def test_has_observable_bulk_add(self):
        api = pyeti.YetiApi(self.url)
        with self.assertRaises(TypeError) as context:
            api.observable_bulk_add()
        self.assertFalse('This is broken' in str(context.exception))

    def test_has_test_connection(self):
        api = pyeti.YetiApi(self.url)
        try:
            api._test_connection()
        except:
            pass

    def test_has__make_post(self):
        api = pyeti.YetiApi(self.url)
        with self.assertRaises(TypeError) as context:
            api._make_post()
        self.assertFalse('This is broken' in str(context.exception))

    def test_has_make_get(self):
        api = pyeti.YetiApi(self.url)
        with self.assertRaises(TypeError) as context:
            api._make_get()
        self.assertFalse('This is broken' in str(context.exception))

    def test_has_make_request(self):
        api = pyeti.YetiApi(self.url)
        with self.assertRaises(TypeError) as context:
            api._make_request()
        self.assertFalse('This is broken' in str(context.exception))

if __name__ == '__main__':
    TestCase.main()
