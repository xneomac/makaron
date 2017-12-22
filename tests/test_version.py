import unittest

from makaron import Version, LocatedVersion
from makaron.exception import BadVersionFormat, BadVersionComponentFormat


class TestVersion(unittest.TestCase):

    def test_creation(self):
        version = Version()
        self.assertEqual(version.major, 0)
        self.assertEqual(version.minor, 0)
        self.assertEqual(version.patch, 0)

    def test_set_major(self):
        version = Version()
        self.assertEqual(version.major, 0)
        version.set_major(5)
        self.assertEqual(version.major, 5)

    def test_set_major_with_negative_number(self):
        version = Version()
        with self.assertRaises(BadVersionComponentFormat):
            version.set_major(-5)

    def test_set_major_with_letter(self):
        version = Version()
        with self.assertRaises(BadVersionComponentFormat):
            version.set_major('a')

    def test_set_minor(self):
        version = Version()
        self.assertEqual(version.minor, 0)
        version.set_minor(5)
        self.assertEqual(version.minor, 5)

    def test_set_minor_with_negative_number(self):
        version = Version()
        with self.assertRaises(BadVersionComponentFormat):
            version.set_minor(-5)

    def test_set_minor_with_letter(self):
        version = Version()
        with self.assertRaises(BadVersionComponentFormat):
            version.set_minor('a')

    def test_set_patch(self):
        version = Version()
        self.assertEqual(version.patch, 0)
        version.set_patch(5)
        self.assertEqual(version.patch, 5)

    def test_set_patch_with_negative_number(self):
        version = Version()
        with self.assertRaises(BadVersionComponentFormat):
            version.set_patch(-5)

    def test_set_patch_with_letter(self):
        version = Version()
        with self.assertRaises(BadVersionComponentFormat):
            version.set_patch('a')

    def test_set_from_string(self):
        version = Version()
        version.set_from_string('1.2.3')
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 3)

    def test_set_from_string_version_empty(self):
        version = Version()
        with self.assertRaises(BadVersionFormat):
            version.set_from_string('')

    def test_set_from_string_version_with_letter(self):
        version = Version()
        with self.assertRaises(BadVersionFormat):
            version.set_from_string('1.2.a')

    def test_set_from_string_version_with_letters(self):
        version = Version()
        with self.assertRaises(BadVersionFormat):
            version.set_from_string('bad version')

    def test_increase_major(self):
        version = Version()
        version.set_from_string('1.2.3')
        version.increase_major()
        self.assertEqual(version.major, 2)
        self.assertEqual(version.minor, 0)
        self.assertEqual(version.patch, 0)

    def test_increase_minor(self):
        version = Version()
        version.set_from_string('1.2.3')
        version.increase_minor()
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 3)
        self.assertEqual(version.patch, 0)

    def test_increase_patch(self):
        version = Version()
        version.set_from_string('1.2.3')
        version.increase_patch()
        self.assertEqual(version.major, 1)
        self.assertEqual(version.minor, 2)
        self.assertEqual(version.patch, 4)

    def test_copy(self):
        version_a = Version()
        version_a.set_from_string('1.2.3')
        version_b = Version()
        self.assertEqual(version_b.major, 0)
        self.assertEqual(version_b.minor, 0)
        self.assertEqual(version_b.patch, 0)
        version_b.copy(version_a)
        self.assertEqual(version_b.major, 1)
        self.assertEqual(version_b.minor, 2)
        self.assertEqual(version_b.patch, 3)


class TestLocatedVersion(unittest.TestCase):

    def test_creation(self):
        file_name = 'filename.py'
        line = 'this is a line'
        version = Version()
        version.set_from_string('1.2.3')

        located_version = LocatedVersion(version, file_name, line)
        self.assertEqual(located_version.version.get(), '1.2.3')
        self.assertEqual(located_version.file_name, 'filename.py')
        self.assertEqual(located_version.line, 'this is a line')
