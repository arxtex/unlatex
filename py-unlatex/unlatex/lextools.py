'''Provides lex_lines command for texbox files

'''

import re

# Some funny lines in texbox files.
'ootnote.1}'
'.......|\\OT1/cmr/m/n/10 f'
'\\0\\ETC.}'
'ite.Kontsevich93}'


# Two regular expression constructors.
def named_group(name, pattern):
    '''Return pattern wrapped as a named group.

    '''
    # Search 'python regex builder class'
    # https://github.com/bruntonspall/regex-builder
    # Brunton's builder source does not contain'<'.

    # TODO: Check name is valid Python identifier.

    return rf'(?P<{name}>{pattern})'

def non_capture(pattern):
    return rf'(?:{pattern})'

# Regular expression patterns.
if False:
    # Give names such as 'write4' and 'kern1'.
    name_pattern = '[a-zA-Z0-9/]+'

# There are two sorts of name patterns.
latex_fontname_pattern = '(?:[A-Z0-9]+/)(?:[a-zA-Z]+/)*(?:[0-9]+)'
tex_command_pattern = '(?:[a-zA-z]+)'

# Combine to producce the name pattern we use.
name_pattern = fr'(?:{latex_fontname_pattern}|{tex_command_pattern})'

# Produce pattern that will lex just one line.
lex_one_line = re.compile(
    ''
    + named_group('path', '[.]*' + r'\|?')
    + r'\\'
    + named_group('name', name_pattern)
    + named_group('args', '.*'),
    ).fullmatch

# GOTCHA: Can't subclass re.Match object.
# >>> class AAA(re.Match):
# >>>     pass
# TypeError: type 're.Match' is not an acceptable base type


def lex_lines(lines):
    '''Iterate of the lexed output of lines. Handles non-match error.
    '''

    # Ensure this is a generator function (returns an iterator).
    if False:
        yield

    path = ''
    for line in lines:

        match = lex_one_line(line)
        if match:
            path = match['path']
            name = match['name']
            args = match['args']
        else:
            name = 'LEXERROR'
            args = line
            path = path         # Remains unchanged

        yield path, name, args
