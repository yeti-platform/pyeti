from unittest import TestCase

import pyeti


class TestAPI(TestCase):
    def test_has_version(self):
        s = pyeti.__version__
        self.assertTrue(isinstance(s, basestring))
