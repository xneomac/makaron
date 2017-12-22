import os, yaml

from .exception import YamlErrorConfigFileParsing, UnknownErrorConfigFileParsing, NoConfigFileFound

config_file_name = '.makaron.yml'

config_file_content = \
'''# {}
# more info at https://makaron.gitlab.io

setup.py: "__version__ = .*"
version.c:
    major: "#define major .*"
    minor: "#define minor .*"
    patch: "#define patch .*"

'''.format(config_file_name)


def generate_config_file():
    with open(config_file_name, 'w') as stream:
        stream.write(config_file_content)


def read_config_file():
    if os.path.isfile(config_file_name):
        with open(config_file_name, 'r') as stream:
            try:
                content = stream.read()
                config = yaml.safe_load(content)
                return config
            except yaml.YAMLError as exc:
                if hasattr(exc, 'problem_mark'):
                    raise YamlErrorConfigFileParsing(exc.problem_mark)
                else:
                    raise UnknownErrorConfigFileParsing()
    else:
        raise NoConfigFileFound()
