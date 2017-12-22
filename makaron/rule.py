import re

from .version import full_version_regex_format, separated_version_regex_format, LocatedVersion, Version
from .config import read_config_file
from .exception import MakaronException


def get_makaron_rules():
    config = read_config_file()
    rules = parse_version_rules(config)
    return rules


def parse_version_rules(config):

    if not type(config) == dict:
        raise Exception('config file should be a dict')

    rules = []
    for file_name, info in config.items():
        parse_version_rule(rules, file_name, info)
    return rules


def parse_version_rule(rules, file_name, info):

    if type(info) == str:
        parse_full_vresion_rule(rules, file_name, info)

    elif type(info) == dict:
        parse_separated_version_rule(rules, file_name, info)

    elif type(info) == list:
        parse_list_version_rule(rules, file_name, info)

    else:
        raise Exception('bad rule type.')


def parse_full_vresion_rule(rules, file_name, info):
    rule = FullVersionRule(file_name, info)
    rules.append(rule)

def parse_list_version_rule(rules, file_name, info):
    for info_item in info:
        parse_version_rule(rules, file_name, info_item)


def parse_separated_version_rule(rules, file_name, info):

    if not 'major' in info:
        raise RuntimeError('missing major rule')
    major = info['major']

    if not 'minor' in info:
        raise RuntimeError('missing minor rule')
    minor = info['minor']

    if not 'patch' in info:
        raise RuntimeError('missing patch rule')
    patch = info['patch']

    rule = SeparatedVersionRule(file_name, major, minor, patch)
    rules.append(rule)


def read_file(filename):
    try:
        stream = open(filename, 'r')
        content = stream.read()
        stream.close()
        return content
    except IOError as e:
        raise(RuntimeError('No such file: \'{0}\''.format(filename)))


def write_file(filename, content):
    try:
        stream = open(filename, 'w')
        stream.write(content)
        stream.close()
        return content
    except IOError as e:
        raise(RuntimeError('Error opening file: \'{0}\''.format(filename)))


def search(regex, content):
    m = re.search(regex, content)
    if m:
        line = m.group(0)
        return line
    else:
        raise Exception('search_line: nothing found\n{}\n\n{}'.format(regex, content))


class FullVersionRule:

    def __init__(self, file_name, version_regex):
        self.version_regex = version_regex
        self.file_name = file_name

    def apply(self, new_version):

        content = read_file(self.file_name)

        version_line = search(self.version_regex, content)
        version_found = search(full_version_regex_format, version_line)

        new_version_line = version_line.replace(version_found, new_version.get())
        content = content.replace(version_line, new_version_line)

        write_file(self.file_name, content)

    def collect(self):

        content = read_file(self.file_name)

        line = search(self.version_regex, content)
        found = search(full_version_regex_format, line)

        version = Version()
        version.set_from_string(found)
        located_version = LocatedVersion(version, self.file_name, '\n  {}\n'.format(line))

        return located_version


class SeparatedVersionRule:

    def __init__(self, file_name, major_regex, minor_regex, patch_regex):
        self.file_name = file_name
        self.major_regex = major_regex
        self.minor_regex = minor_regex
        self.patch_regex = patch_regex

    def apply(self, new_version):

        content = read_file(self.file_name)
        version_components = new_version.get().split('.')

        major_component = version_components[0]

        major_line = search(self.major_regex, content)
        major_found = search(separated_version_regex_format, major_line)
        new_major_line = major_line.replace(major_found, major_component)
        content = content.replace(major_line, new_major_line)

        minor_component = version_components[1]
        minor_line = search(self.minor_regex, content)
        minor_found = search(separated_version_regex_format, minor_line)
        new_minor_line = minor_line.replace(minor_found, minor_component)
        content = content.replace(minor_line, new_minor_line)

        patch_component = version_components[2]
        patch_line = search(self.patch_regex, content)
        patch_found = search(separated_version_regex_format, patch_line)
        new_patch_line = patch_line.replace(patch_found, patch_component)
        content = content.replace(patch_line, new_patch_line)

        write_file(self.file_name, content)

    def collect(self):

        content = read_file(self.file_name)

        try:
            major_line = search(self.major_regex, content)
            major_found = search(separated_version_regex_format, major_line)
        except Exception as e:
            raise MakaronException('Could not find the major component in \'{}\' with \'{}\' regex.'.format(self.file_name, self.major_regex))

        try:
            minor_line = search(self.minor_regex, content)
            minor_found = search(separated_version_regex_format, minor_line)
        except Exception as e:
            raise MakaronException('Could not find the minor component in \'{}\' with \'{}\' regex.'.format(self.file_name, self.minor_regex))

        try:
            patch_line = search(self.patch_regex, content)
            patch_found = search(separated_version_regex_format, patch_line)
        except Exception as e:
            raise MakaronException('Could not find the patch component in \'{}\' with \'{}\' regex.'.format(self.file_name, self.patch_regex))


        version = Version()
        version.set_from_string('{0}.{1}.{2}'.format(major_found, minor_found, patch_found))

        line = '\n  major: {}\n  minor: {}\n  patch: {}\n'.format(major_line, minor_line, patch_line)
        located_version = LocatedVersion(version, self.file_name, line)

        return located_version
