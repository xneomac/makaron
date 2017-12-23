import unittest
import os, tempfile, shutil

from makaron.tools import *


class TestTools(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.current = os.getcwd()
        os.chdir(self.tmp)

    def tearDown(self):
        os.chdir(self.current)
        shutil.rmtree(self.tmp)

    def test_write_file(self):
        file_name = 'file.py'
        content = 'content of the file'
        write_file(file_name, content)
        self.assertTrue(os.path.exists(file_name))
        with open(file_name, 'r') as stream:
            content_read = stream.read()
            self.assertEqual(content_read, content)

    def test_read_file(self):
        file_name = 'file.py'
        content = 'content of the file'
        with open(file_name, 'w') as stream:
            stream.write(content)
        content_read = read_file(file_name)
        self.assertEqual(content_read, content)

    def test_read_file_missing_file(self):
        file_name = 'file.py'
        with self.assertRaises(RuntimeError):
            read_file(file_name)

    def test_search(self):
        regex = '[0-9]+\.[0-9]+\.[0-9]+'
        content = 'version = 0.1.2'
        result = search(regex, content)
        self.assertEqual(result, ['0.1.2'])

    def test_search_no_match(self):
        regex = '[0-9]+\.[0-9]+\.[0-9]+'
        content = 'version'
        result = search(regex, content)
        self.assertEqual(result, [])

    def test_search_multiple(self):
        regex = '[0-9]+\.[0-9]+\.[0-9]+'
        content = 'version = 0.1.2\nversion = 5.2.0'
        result = search(regex, content)
        self.assertEqual(result, ['0.1.2', '5.2.0'])

    def test_search_one(self):
        regex = '[0-9]+\.[0-9]+\.[0-9]+'
        content = 'version = 0.1.2'
        result = search_one(regex, content)
        self.assertEqual(result, '0.1.2')

    def test_search_one_no_match(self):
        regex = '[0-9]+\.[0-9]+\.[0-9]+'
        content = 'version'
        with self.assertRaises(RuntimeError):
            result = search_one(regex, content)

    def test_search_one_multiple(self):
        regex = '[0-9]+\.[0-9]+\.[0-9]+'
        content = 'version = 0.1.2\nversion = 5.2.0'
        with self.assertRaises(RuntimeError):
            search_one(regex, content)
