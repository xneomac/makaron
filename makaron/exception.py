class MakaronException(Exception):
    pass


no_config_file_found_message = \
'''
No '.makaron.yml' file found.
Create one by executing 'makaron --generate-config'.
'''

class NoConfigFileFound(MakaronException):
    def __init__(self):
        message = no_config_file_found_message
        super(NoConfigFileFound, self).__init__(message)


unknown_error_config_file_parsing_message = \
'''
Unknown error during config file parsing.
'''

class UnknownErrorConfigFileParsing(MakaronException):
    def __init__(self):
        message = unknown_error_config_file_parsing_message
        super(UnknownErrorConfigFileParsing, self).__init__(message)


yaml_error_config_file_parsing_message = \
'''
Yaml error during config file parsing.
Error position: ({}:{})
'''

class YamlErrorConfigFileParsing(MakaronException):
    def __init__(self, mark):
        message = yaml_error_config_file_parsing_message.format(mark.line+1, mark.column+1)
        super(YamlErrorConfigFileParsing, self).__init__(message)


versions_found_are_different_message = \
'''
Versions found are different.
'''

class VersionsFoundAreDifferent(MakaronException):
    def __init__(self):
        message = versions_found_are_different_message
        super(VersionsFoundAreDifferent, self).__init__(message)
