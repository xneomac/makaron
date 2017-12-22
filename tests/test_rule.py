import unittest
import os, tempfile, shutil

from makaron.rule import *
from makaron.version import Version
from makaron.exception import MissingVersionInRule

class TestRule(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.current = os.getcwd()
        os.chdir(self.tmp)

    def tearDown(self):
        os.chdir(self.current)
        shutil.rmtree(self.tmp)

    def test_creation(self):
        file_name = 'file.py'
        version_regex = 'version = [version]'

        rule = Rule(file_name, version_regex)

        self.assertEqual(rule.file_name, file_name)
        self.assertEqual(rule.version_regex, 'version = [0-9]+\\.[0-9]+\\.[0-9]+')

    def test_creation_no_version(self):
        file_name = 'file.py'
        version_regex = 'version = '

        with self.assertRaises(MissingVersionInRule):
            rule = Rule(file_name, version_regex)

    def test_collect(self):
        file_name = 'file.py'
        version_regex = 'version = [version]'
        content = 'version = 0.2.5'

        with open(file_name, 'w') as stream:
            stream.write(content)

        rule = Rule(file_name, version_regex)
        versions = rule.collect()

        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0].version.get(), '0.2.5')

    def test_collect_multiple(self):
        file_name = 'file.py'
        version_regex = 'version = [version]'
        content = 'version = 0.2.5\nversion = 0.4.8'

        with open(file_name, 'w') as stream:
            stream.write(content)

        file_name = 'file.py'
        rule = Rule(file_name, version_regex)
        versions = rule.collect()

        self.assertEqual(len(versions), 2)
        self.assertEqual(versions[0].version.get(), '0.2.5')
        self.assertEqual(versions[1].version.get(), '0.4.8')

    def test_apply(self):
        version = Version('0.5.4')
        file_name = 'file.py'
        version_regex = 'version = [version]'
        content = 'version = 0.2.5'
        content_expected = 'version = 0.5.4'

        with open(file_name, 'w') as stream:
            stream.write(content)

        rule = Rule(file_name, version_regex)
        rule.apply(version)

        with open(file_name, 'r') as stream:
            content = stream.read()
            self.assertEqual(content, content_expected)

    def test_apply_multiple(self):
        version = Version('0.5.4')
        file_name = 'file.py'
        version_regex = 'version = [version]'
        content = 'version = 0.2.5\nversion = 0.4.8'
        content_expected = 'version = 0.5.4\nversion = 0.5.4'

        with open(file_name, 'w') as stream:
            stream.write(content)

        rule = Rule(file_name, version_regex)
        rule.apply(version)

        with open(file_name, 'r') as stream:
            content = stream.read()
            self.assertEqual(content, content_expected)
