import typing

import interpret

"""
read
validate
tokenize
"""

def read_file(file_name:str) -> str:
    """
    Read input file and output text

    :param file_name: name of file containing program
    :returns: string of file content, raw
    """
    pass

def is_balanced(raw:str) -> bool:
    """
    Validate a program has an identical number of yin and yang values

    :param raw: raw text of the file
    :returns: True if the program is balanced
    """
    pass

def make_stanzas(raw:str) -> typing.List[str]:
    """
    Take raw file contents and produce a list of stanza strings

    :param raw: raw text of the file
    :returns: list of stanza strings, stanzas
    :raises SyntaxError: if there aren't proper stanzas
    """
    pass

def is_valid_haiku(stanza:str) -> bool:
    """
    Validate a haiku follows the 5-7-5 syllable pattern

    :param stanza: single stanza to validate
    :returns: True if the stanza is valid
    """
    pass

def remove_comments(raw:str) -> str:
    """
    Remove comments from a program

    :param raw: raw text of the file
    :returns: raw text without the comments
    """
    pass

def make_tokens(raw_valid:str) -> typing.List[interpret.Token]:
    """
    Turn the syntactically valid raw text into a list of tokens

    :param raw_valid: raw text post validation
    :returns: list of tokens
    """
    pass

def parse(file_name:str) -> typing.List[interpret.Token]:
    """
    Given a filename, produce the tokens of that program

    :param file_name: name of program input file
    :returns: list of tokens
    """
    pass

