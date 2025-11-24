import typing
from enum import Enum


class TokenType(Enum):
    HEAVEN = 0
    PROMOTE = 1
    DEMOTE = 2
    BLOSSOM = 3
    RISE = 4
    FALL = 5
    LISTEN = 6
    SPEAK = 7
    COUNT = 8
    CREATE = 9
    DESTROY = 10
    FEAR = 11
    LOVE = 12
    BECOME = 13
    LIKE = 14
    NEGATIVE = 15
    OPERATE = 16
    PUNC = 17
    INT = 18
    VAR = 19
    RAND = 20
    COMMA = 21


class ElementType(Enum):
    WOOD = 0
    FIRE = 1
    EARTH = 2
    METAL = 3
    WATER = 4


class Token:
    t: TokenType = None
    value:typing.Any = None

    def __init__(self, t, value=None):
        self.t = t
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, Token):
            return NotImplemented
        return self.t == other.t and self.value == other.value

    def __repr__(self):
        return f"Token(t='{self.t}', value='{self.value}')"


class VariableToken:
    name:str = None
    init_element:ElementType = None

    def __init__(self, name, init_element:ElementType=ElementType.EARTH):
        self.name = name
        self.init_element = init_element

    def __eq__(self, other):
        if not isinstance(other, VariableToken):
            return NotImplemented
        return self.name == other.name and self.init_element == other.init_element
