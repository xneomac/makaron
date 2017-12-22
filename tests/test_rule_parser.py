import unittest
import os, tempfile, shutil

from makaron.rule_parser import *
from makaron.exception import ConfigBadFormat, RuleBadFormat


class TestRuleParser(unittest.TestCase):

    def test_parse_version_rules(self):
        config = {
            'setup.py': '[version]'}
        rules = parse_version_rules(config)
        self.assertEqual(len(rules), 1)

    def test_parse_version_rules_multiple(self):
        config = {
            'setup.py': '[version]',
            'script/makaron': '__version__ = [version]'}
        rules = parse_version_rules(config)
        self.assertEqual(len(rules), 2)

    def test_parse_version_rules_same_file_different_version(self):
        config = {
            'setup.py': ['[version]', '__version__ = [version]']}
        rules = parse_version_rules(config)
        self.assertEqual(len(rules), 2)

    def test_parse_version_rules_string(self):
        config = 'setup.py'
        with self.assertRaises(ConfigBadFormat):
            rules = parse_version_rules(config)

    def test_parse_version_rules_list(self):
        config = []
        with self.assertRaises(ConfigBadFormat):
            rules = parse_version_rules(config)

    def test_parse_version_rules_with_bad_rule_integer(self):
        config = {
            'setup.py': 0}
        with self.assertRaises(RuleBadFormat):
            rules = parse_version_rules(config)

    def test_parse_version_rules_with_bad_rule_dict(self):
        config = {
            'setup.py': {}}
        with self.assertRaises(RuleBadFormat):
            rules = parse_version_rules(config)

    def test_parse_version_rules_with_bad_rule_none(self):
        config = {
            'setup.py': None}
        with self.assertRaises(RuleBadFormat):
            rules = parse_version_rules(config)

    def test_parse_version_rules_with_bad_list_integer(self):
        config = {
            'setup.py': [0]}
        with self.assertRaises(RuleBadFormat):
            rules = parse_version_rules(config)

    def test_parse_version_rules_with_bad_list_dict(self):
        config = {
            'setup.py': [{}]}
        with self.assertRaises(RuleBadFormat):
            rules = parse_version_rules(config)

    def test_parse_version_rules_with_bad_list_none(self):
        config = {
            'setup.py': [None]}
        with self.assertRaises(RuleBadFormat):
            rules = parse_version_rules(config)
