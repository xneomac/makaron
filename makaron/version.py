full_version_regex_format = '[0-9]+\.[0-9]+\.[0-9]+'
separated_version_regex_format = '[0-9]+'


class Version():
    def __init__(self):
        self.major = 0
        self.minor = 0
        self.patch = 0

    def copy(self, version):
        self.major = version.major
        self.minor = version.minor
        self.patch = version.patch

    def set_from_string(self, version):
        version_spiltted = version.split('.')
        self.major = int(version_spiltted[0])
        self.minor = int(version_spiltted[1])
        self.patch = int(version_spiltted[2])

    def set_major(self, major):
        self.major = major

    def set_minor(self, minor):
        self.minor = minor

    def set_patch(self, patch):
        self.patch = patch

    def increase_major(self):
        self.major += 1
        self.minor = 0
        self.patch = 0

    def increase_minor(self):
        self.minor += 1
        self.patch = 0

    def increase_patch(self):
        self.patch += 1

    def get(self):
        return '{}.{}.{}'.format(self.major, self.minor, self.patch)


class LocatedVersion():
    def __init__(self, version, file_name, line):
        self.version = version
        self.file_name = file_name
        self.line = line
