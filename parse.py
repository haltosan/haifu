import typing
from enum import Enum

import interpret

"""
read
validate text
tokenize
validate tokens
"""

class ParserTokenType(Enum):
    COMMA = 100

class ParserToken:
    t:ParserTokenType = None
    value:typing.Any = None

    def __init__(self, t, value=None):
        self.t = t
        self.value = value

def read_file(file_name:str) -> str:
    """
    Read input file and output text

    :param file_name: name of file containing program
    :returns: string of file content, raw
    """
    try:
        with open(file_name, 'r') as file:
            ret = file.read()
    except FileNotFoundError:
        return ''
    return ret

def make_stanzas(raw:str) -> typing.List[str]:
    """
    Take raw file contents and produce a list of stanza strings

    :param raw: raw text of the file
    :returns: list of stanza strings, stanzas
    :raises SyntaxError: if there aren't proper stanzas
    """
    lines = raw.split('\n')
    if len(lines) == 1 and lines[0] == '':
        return []
    if len(lines) % 4 != 0 and (len(lines) + 1) % 4 != 0:
        raise SyntaxError('Improper number of lines')

    stanzas = []
    i = 0
    buf = []
    for line in lines:
        i += 1
        if i % 4 == 0:
            if line != '':
                raise SyntaxError('No blank line between stanzas')
            continue
        buf.append(line)
        if i % 4 == 3:
            stanzas.append('\n'.join(buf))
            buf = []
    return stanzas

def is_valid_haiku(stanza:str) -> bool:
    """
    Validate a haiku follows the 5-7-5 syllable pattern

    :param stanza: single stanza to validate
    :returns: True if the stanza is valid
    """
    pass

def make_tokens(raw_valid:str) -> typing.List[ParserToken]:
    """
    Turn the syntactically valid raw text into a list of tokens

    :param raw_valid: raw text post validation
    :returns: list of parser tokens
    """
    pass

def is_balanced(tokens:typing.List[ParserToken]) -> bool:
    """
    Validate a program has an identical number of yin and yang values

    :param tokens: list of parser tokens
    :returns: True if the program is balanced
    """
    pass

def remove_comments(tokens:typing.List[ParserToken]) -> typing.List[interpret.Token]:
    """
    Remove comments from a program

    :param tokens: list of parser tokens
    :returns: list of tokens minus the comments
    """
    pass

def parse(file_name:str) -> typing.List[interpret.Token]:
    """
    Given a filename, produce the tokens of that program

    :param file_name: name of program input file
    :returns: list of tokens
    """
    pass

