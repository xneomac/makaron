import unittest
import os, tempfile, shutil

from makaron import read_config_file, generate_config_file, config_file_name, config_file_content
from makaron.exception import NoConfigFileFound, YamlErrorConfigFileParsing, YamlErrorConfigFileBadType

bad_config_file='''
test_creation
    - test
    - doekdoe: [
'''

bad_type_config_file='''
test_creation
'''

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.current = os.getcwd()
        os.chdir(self.tmp)

    def tearDown(self):
        os.chdir(self.current)
        shutil.rmtree(self.tmp)

    def test_generate_config_file(self):
        generate_config_file()
        with open(config_file_name, 'r') as stream:
            content = stream.read()
            self.assertEqual(content, config_file_content)

    def test_read_config_file(self):
        generate_config_file()
        config = read_config_file()
        self.assertTrue(isinstance(config, dict))

    def test_read_config_file_no_file(self):
        with self.assertRaises(NoConfigFileFound):
            read_config_file()

    def test_read_config_file_bad_yaml(self):
        with open(config_file_name, 'w') as stream:
            stream.write(bad_config_file)
        with self.assertRaises(YamlErrorConfigFileParsing):
            config = read_config_file()

    def test_read_config_file_bad_type_yaml(self):
        with open(config_file_name, 'w') as stream:
            stream.write(bad_type_config_file)
        with self.assertRaises(YamlErrorConfigFileBadType):
            config = read_config_file()
