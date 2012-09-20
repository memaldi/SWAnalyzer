import unittest
from ckan_api import CKAN
import json

class CKANTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.ckan = CKAN('http://www.thedatahub.org')

    @classmethod
    def tearDownClass(self):
        self.ckan.close()

    def test_get_datasets_from_group(self):
        f = open('test_group_json')
        s = f.read()
        f.close()
        expected_datasets = eval(s)
        result_datasets = self.ckan.get_datasets_from_group('lodcloud')
        self.assertEqual(result_datasets, expected_datasets)


if __name__ == '__main__':
    unittest.main()
