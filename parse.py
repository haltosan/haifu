import typing
from enum import Enum

import number_parser
from syllables import estimate
import cmudict

import interpret
from interpret import TokenType, ElementType, VariableToken

"""
read
validate text
tokenize
validate tokens
"""

vulgar_words_full = ['cum', 'dick', 'bitch', 'ass', 'anal', 'shit']
vulgar_words_partial = ['fuck', 'cunt', 'cock', 'pussy', 'penis']

c_dict = cmudict.dict()

def count(w: str) -> int:
    """Count syllables in a word"""
    # based on https://datascience.stackexchange.com/a/24865
    if w in c_dict:
        return [len(list(y for y in x if y[-1].isdigit())) for x in c_dict[w.lower()]][0]
    return estimate(w)

def count_line(line:str) -> typing.List[int]:
    line = line.replace('-', ' ')  # split hyphenated words
    words = line.split(' ')
    return [count(word) for word in words]

class ParserTokenType(Enum):
    COMMA = 100

class ParserToken:
    t:ParserTokenType = None
    value:typing.Any = None

    def __init__(self, t, value=None):
        self.t = t
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, ParserToken):
            return NotImplemented
        return self.t == other.t and self.value == other.value

    def __repr__(self):
        return f"ParserToken(t='{self.t}', value='{self.value}')"

number_conversion = {'no':'0', 'none':'0',
                     'a':'1', 'an':'1',
                     'couple':'2',
                     'dozen':'12',
                     'century':'100'}
heaven_token = [TokenType.HEAVEN, ['heaven', 'nirvana', 'enlightenment', 'harmony']]
promote_token = [TokenType.PROMOTE, ['promote', 'more', 'increase', 'wax']]
demote_token = [TokenType.DEMOTE, ['demote', 'less', 'reduce', 'wane']]
blossom_token = [TokenType.BLOSSOM, ['blossom', 'flower', 'petal']]
rise_token = [TokenType.RISE, ['rise', 'float', 'ascend', 'up']]
fall_token = [TokenType.FALL, ['fall', 'drop', 'descend', 'down']]
listen_token = [TokenType.LISTEN, ['listen', 'hear', 'see']]
speak_token = [TokenType.SPEAK, ['speak', 'say', 'draw']]
count_token = [TokenType.COUNT, ['count', 'number', 'age']]
create_token = [TokenType.CREATE, ['create', 'produce', 'build']]
destroy_token = [TokenType.DESTROY, ['destroy', 'damage', 'kill']]
fear_token = [TokenType.FEAR, ['fear', 'hate', 'doubt']]
love_token = [TokenType.LOVE, ['love', 'desire', 'regard']]
become_token = [TokenType.BECOME, ['become', 'reach', 'achieve']]
like_token = [TokenType.LIKE, ['like', 'as', 'is', 'resemble']]
negative_token = [TokenType.NEGATIVE, ['negative', 'not', 'deny']]
operate_token = [TokenType.OPERATE, ['operate', 'examine', 'study']]
rand_token = [TokenType.RAND, ['some', 'few', 'many']]

basic_words = [heaven_token, promote_token, demote_token, blossom_token, rise_token, fall_token, listen_token, speak_token, count_token, create_token, destroy_token, fear_token, love_token, become_token, like_token, negative_token, operate_token, rand_token]

wood = [ElementType.WOOD, ['wood', 'tree', 'grass', 'cherry', 'oak']]
fire = [ElementType.FIRE, ['fire', 'flame', 'ash', 'smoke', 'embers']]
earth = [ElementType.EARTH, ['earth', 'soil', 'mountain', 'rock', 'plain']]
metal = [ElementType.METAL, ['metal', 'sword', 'iron', 'plough', 'knife']]
water = [ElementType.WATER, ['water', 'rain', 'snow', 'river', 'ice']]
elements = [wood, fire, earth, metal, water]


def get_element_type(word:str) -> ElementType:
    for element in elements:
        if word in element[1]:
            return element[0]
    return ElementType.EARTH


def word_to_token(word:str) -> ParserToken:
    if word == ',':
        return ParserToken(ParserTokenType.COMMA)
    word = word.lower()
    # convert numbers
    word = number_parser.parse(word)  # convert number word to number literal
    if word in number_conversion:
        word = number_conversion[word]
    try:
        value = int(word)
        return ParserToken(TokenType.INT, value)
    except ValueError:
        pass
    # convert basic words
    for keyword in basic_words:
        if word in keyword[1]:
            return ParserToken(keyword[0])
    # else variable
    element_t = get_element_type(word)
    return ParserToken(TokenType.VAR, VariableToken(word, element_t))

def read_file(file_name:str) -> str:
    """
    Read input file and output text

    :param file_name: name of file containing program
    :returns: string of file content, raw
    """
    with open(file_name, 'r') as file:
        ret = file.read()
    return ret

def find_vulgar(raw:str) -> typing.Optional[str]:
    """
    Validate a program doesn't contain vulgar words

    :param raw: raw text input
    :returns: True if the program contains vulgar words
    """
    for vulgar in vulgar_words_partial:
        if vulgar in raw:
            return vulgar
    raw = raw.replace('\n', ' ').replace('-', ' ')
    for word in raw.split(' '):
        if word in vulgar_words_full:
            return word
    return None

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
    lines = stanza.split('\n')
    counts = [sum(count_line(line)) for line in lines]
    return counts == [5, 7, 5]

def make_tokens(raw_valid:str) -> typing.List[ParserToken]:
    """
    Turn the syntactically valid raw text into a list of tokens

    :param raw_valid: raw text post validation
    :returns: list of parser tokens
    """
    raw_valid = raw_valid.replace('-\n', '-')  # connect hyphenated words across lines
    raw_valid = raw_valid.replace('\n', ' ')  # remove newlines
    raw_valid = raw_valid.replace('  ', ' ')  # remove blank lines
    words = raw_valid.split(' ')
    tokens = []
    for word in words:
        if ',' in word:
            tokens.append(word_to_token(word[:-1]))
            tokens.append(word_to_token(','))
        else:
            tokens.append(word_to_token(word))
    return tokens

def is_balanced(tokens:typing.List[ParserToken]) -> bool:
    """
    Validate a program has an identical number of yin and yang values

    :param tokens: list of parser tokens
    :returns: True if the program is balanced
    """
    yin = 0
    yang = 0
    for token in tokens:
        if token.t == TokenType.INT:
            if interpret.yin_or_yang(token.value) == interpret.YIN:
                yin += 1
            else:
                yang += 1
    return yin == yang

def remove_comments(tokens:typing.List[ParserToken]) -> typing.List[interpret.Token]:
    """
    Remove comments from a program

    :param tokens: list of parser tokens
    :returns: list of tokens minus the comments
    """
    new_tokens = []
    in_comment = False
    for token in tokens:
        if token.t == ParserTokenType.COMMA:
            in_comment = not in_comment
        else:
            if not in_comment:
                t = interpret.Token(token.t, token.value)
                new_tokens.append(t)
    return new_tokens

def parse(file_name:str) -> typing.List[interpret.Token]:
    """
    Given a filename, produce the tokens of that program

    :param file_name: name of program input file
    :raises SyntaxError: if the program is syntactically invalid
    :raises FileNotFoundError: if input file does not exist
    :returns: list of tokens
    """
    raw = read_file(file_name)

    vulgar = find_vulgar(raw)
    if vulgar is not None:
        raise SyntaxError('Program contains vulgar word: ' + vulgar)
    try:
        stanzas = make_stanzas(raw)
    except SyntaxError as e:
        raise e
    for stanza in stanzas:
        if not is_valid_haiku(stanza):
            raise SyntaxError('Not valid haiku:\n' + stanza)

    tokens = make_tokens(raw)
    if not is_balanced(tokens):
        raise SyntaxError('Yin and yang are not balanced')
    return remove_comments(tokens)

