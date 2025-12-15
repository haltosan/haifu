"""
The interpreter layer

This is responsible for program behavior
"""

import select
from math import ceil, floor
from enum import Enum
import typing
import sys
from random import randint

import haifu_common
import parse
from haifu_common import TokenType, ElementType, Token, VariableToken

YIN: int = 2
YANG: int = 1

RAND_MIN: int = 0
RAND_MAX: int = 2**32


class ElementRelationship(Enum):
    """
    Enum signifying how 2 elements are related
    """
    CREATE = 0
    DESTROY = 1
    FEAR = 2
    LOVE = 3
    SAME = 4


class VariableStruct:
    """
    How variables are stored in the data dict
    """
    element: ElementType = None
    value: typing.Any = None

    def __init__(self, value: typing.Any, element: ElementType):
        self.element = element
        self.value = value


data: typing.Dict[str, VariableStruct] = dict()

def init_rand(x: typing.Any) -> typing.Any:
    """
    Init numbers that are possibly rand
    
    :param x: input token
    :return: A random value if x is RAND, else x
    """
    if isinstance(x, Token) and x.t == TokenType.RAND:
        return randint(RAND_MIN, RAND_MAX)
    return x

def strive_num(x: typing.Union[int, float]) -> int:
    """
    Calculate what the number is striving for
    
    :param x: number
    :return: what x is striving for
    """
    if isinstance(x, int):
        if x < 0:
            return x - 1
        return x + 1
    if x > 0:
        return ceil(x)
    return floor(x)

def yin_or_yang(x: typing.Any) -> typing.Optional[int]:
    """
    Determine the yin or yang quality of the input
    
    :param x: input value
    :return: optionally YIN/YANG if x is a number
    """
    x = init_rand(x)
    if not isinstance(x, (int, float)):
        return None
    if isinstance(x, float):
        x = strive_num(x)
    return YIN if x % 2 == 0 else YANG

def element_relationship(element_a: ElementType, element_b: ElementType =None, relationship_type:ElementRelationship=None) -> typing.Optional[typing.Union[
    ElementType, ElementRelationship]]:
    """
    Interface with elemental relationships
    
    :param element_a: element a
    :param element_b: optional element b
    :param relationship_type: optional element relationship
    :return: if a and relationship is specified, return element b; else return relationship between a and b
    """
    create_relationship = {
        ElementType.EARTH: ElementType.METAL,
        ElementType.METAL: ElementType.WATER,
        ElementType.WATER: ElementType.WOOD,
        ElementType.WOOD: ElementType.FIRE,
        ElementType.FIRE: ElementType.EARTH
    }
    destroy_relationship = {
        ElementType.EARTH: ElementType.WATER,
        ElementType.WATER: ElementType.FIRE,
        ElementType.FIRE: ElementType.METAL,
        ElementType.METAL: ElementType.WOOD,
        ElementType.WOOD: ElementType.EARTH
    }
    love_relationship = {
        ElementType.EARTH: ElementType.FIRE,
        ElementType.FIRE: ElementType.WOOD,
        ElementType.WOOD: ElementType.WATER,
        ElementType.WATER: ElementType.METAL,
        ElementType.METAL: ElementType.EARTH
    }
    fear_relationship = {
        ElementType.EARTH: ElementType.WOOD,
        ElementType.WOOD: ElementType.METAL,
        ElementType.METAL: ElementType.FIRE,
        ElementType.FIRE: ElementType.WATER,
        ElementType.WATER: ElementType.EARTH
    }
    relationship = {
        ElementRelationship.CREATE:create_relationship,
        ElementRelationship.DESTROY:destroy_relationship,
        ElementRelationship.LOVE:love_relationship,
        ElementRelationship.FEAR:fear_relationship
    }

    a_b_relationship = {(a,relationship[t][a]):t for t in relationship for a in relationship[t]}

    if element_b is None:
        return relationship[relationship_type][element_a]
    try:
        ret = a_b_relationship[element_a, element_b]
        return ret
    except KeyError:
        return None

def op(a: Token, b: Token) -> typing.Optional[typing.Union[float, int]]:
    """
    Operate instruction
    
    :param a: variable token a
    :param b: variable token b
    :return: result of the operation between a and b
    """
    try:
        a_name:str = a.value.name
        b_name:str = b.value.name
    except AttributeError:
        return None
    try:
        a_var:VariableStruct = data[a_name]
    except KeyError:
        return None
    a_type = a_var.element
    a_val = init_rand(a_var.value)
    if not isinstance(a_val, (int, float)):
        return None
    try:
        b_var = data[b_name]
    except KeyError:
        return None
    b_type = b_var.element
    b_val = init_rand(b_var.value)
    if not isinstance(b_var.value, (int, float)):
        return None
    match element_relationship(b_type, a_type):
        case ElementRelationship.CREATE:
            return a_val + b_val
        case ElementRelationship.DESTROY:
            return a_val - b_val
        case ElementRelationship.FEAR:
            return a_val / b_val
        case ElementRelationship.LOVE:
            return a_val * b_val
        case _:
            if yin_or_yang(a_val) == YANG and yin_or_yang(b_val) == YANG:
                return YANG
            return YIN

def run(bureaucracy: typing.List[Token], debug=False):
    """
    Interpret a program
    
    :param bureaucracy: input program
    :param debug: if debug information should be outputted
    """
    global data
    input_buffer: typing.List[str] = []

    bureaucrat = -1  # deal with fence posting
    delegate = 0
    def dprint(txt):
        if debug:
            print('\t', txt, file=sys.stderr)

    while bureaucrat < len(bureaucracy):
        bureaucrat += 1
        if delegate < 0:
            delegate = 0
        if bureaucrat < 0:
            bureaucrat = 0
        if delegate > bureaucrat:
            delegate = bureaucrat
        if bureaucrat >= len(bureaucracy):
            return
        rung: Token = bureaucracy[bureaucrat]
        match rung.t:
            case TokenType.HEAVEN:
                dprint('halt')
                return

            case TokenType.PROMOTE | TokenType.DEMOTE:
                dprint('promote/demote')
                if rung.t == TokenType.DEMOTE:
                    sign = -1
                else:
                    sign = 1
                d_rung: Token = bureaucracy[delegate]
                diff:int = 0
                match d_rung.t:
                    case TokenType.INT:
                        diff = d_rung.value
                    case TokenType.VAR:
                        var_name:str = d_rung.value.name
                        try:
                            var:VariableStruct = data[var_name]
                        except KeyError:
                            continue
                        value = var.value
                        if type(value) is int:
                            diff = value
                        else:
                            continue
                bureaucrat += diff * sign
                bureaucrat -= 1  # compensate for natural ascension

            case TokenType.BLOSSOM:
                dprint('blossom')
                d_rung = bureaucracy[delegate]
                jump_val:int = 0
                match d_rung.t:
                    case TokenType.INT:
                        jump_val = d_rung.value
                    case TokenType.VAR:
                        var_name:str = d_rung.value.name
                        try:
                            var:VariableStruct = data[var_name]
                        except KeyError:
                            continue
                        value = var.value
                        if type(value) is int:
                            jump_val = value
                        else:
                            continue
                    case _:
                        continue
                jump_val = abs(jump_val)
                if yin_or_yang(jump_val) is YIN:
                    jump_val = -jump_val
                bureaucrat += jump_val
                bureaucrat -= 1  # compensate for natural progression

            case TokenType.RISE | TokenType.FALL:
                dprint('rise/fall')
                if rung.t == TokenType.FALL:
                    sign = -1
                else:
                    sign = 1

                lower: Token = bureaucracy[bureaucrat - 1]
                diff:int = 1
                match lower.t:
                    case TokenType.INT:
                        diff = lower.value
                    case TokenType.VAR:
                        var_name:str = lower.value.name
                        try:
                            var:VariableStruct = data[var_name]
                        except KeyError:
                            continue
                        value = var.value
                        if type(value) is int:
                            diff = value
                        else:
                            continue
                delegate += diff * sign

            case TokenType.LISTEN:
                dprint('listen')
                raw = ''
                if len(input_buffer) > 0:
                    raw = input_buffer.pop(0)
                else:
                    try:
                        line = input().split(' ')
                        raw = line.pop(0)
                        input_buffer = input_buffer + line
                    except EOFError:
                        # no data, move rung to bottom
                        rung_above = bureaucracy.pop(bureaucrat+1)
                        bureaucracy.insert(0, rung_above)
                        bureaucrat += 1
                        delegate += 1
                        continue
                parse_token = parse.word_to_token(raw)
                if parse_token.t == haifu_common.TokenType.COMMA:
                    continue
                bureaucracy.insert(0, Token(parse_token.t, parse_token.value))
                bureaucrat += 1
                delegate += 1

            case TokenType.COUNT | TokenType.SPEAK:
                if rung.t == TokenType.SPEAK:
                    dprint('speak')
                    def cast(x):
                        return chr(x)
                else:
                    dprint('count')
                    def cast(x):
                        return x

                d_rung: Token = bureaucracy[delegate]
                match d_rung.t:
                    case TokenType.INT:
                        print(cast(d_rung.value), end='')
                    case TokenType.VAR:
                        var_name:str = d_rung.value.name
                        try:
                            var:VariableStruct = data[var_name]
                        except KeyError:
                            continue
                        value = init_rand(var.value)
                        if isinstance(value, (int, float)):
                            print(cast(value), end='')

            case TokenType.CREATE | TokenType.DESTROY | TokenType.FEAR | TokenType.LOVE:
                dprint('element change')
                d_rung: Token = bureaucracy[delegate]
                if d_rung.t != TokenType.VAR:
                    continue
                var_name:str = d_rung.value.name
                try:
                    current_element: ElementType = data[var_name].element
                except KeyError:
                    continue
                relationship:ElementRelationship = ElementRelationship.CREATE
                match rung.t:
                    case TokenType.CREATE:
                        relationship = ElementRelationship.CREATE
                    case TokenType.DESTROY:
                        relationship = ElementRelationship.DESTROY
                    case TokenType.FEAR:
                        relationship = ElementRelationship.FEAR
                    case TokenType.LOVE:
                        relationship = ElementRelationship.LOVE
                data[var_name].element = element_relationship(
                    element_a=current_element, relationship_type=relationship)

            case TokenType.BECOME:
                dprint('become')
                d_rung: Token = bureaucracy[delegate]
                match d_rung.t:
                    case TokenType.INT:
                        value:int = d_rung.value
                        if value == 0:
                            bureaucracy[delegate] = Token(TokenType.HEAVEN)
                        else:
                            bureaucracy[delegate].value = strive_num(value)
                    case TokenType.VAR:
                        var_name:str = d_rung.value.name
                        try:
                            var:VariableStruct = data[var_name]
                        except KeyError:
                            continue
                        value = init_rand(var.value)
                        if isinstance(value, (int, float)):
                            if value == 0:
                                bureaucracy[delegate] = Token(TokenType.HEAVEN)
                                continue
                            else:
                                data[var_name].value = strive_num(value)
                            var_type: ElementType = var.element
                            data[var_name].element = element_relationship(element_a=var_type, relationship_type=ElementRelationship.CREATE)

            case TokenType.LIKE:
                dprint('like')
                change: Token = bureaucracy[bureaucrat - 1]
                if change.t != TokenType.VAR:
                    continue
                change_var_name:str = change.value.name
                if change_var_name not in data:
                    continue
                search:int = delegate
                while search >= 0:
                    d_rung: Token = bureaucracy[search]
                    match d_rung.t:
                        case TokenType.INT:
                            data[change_var_name].value = d_rung.value
                            break
                        case TokenType.VAR:
                            d_rung_var_name:str = d_rung.value.name
                            value = init_rand(data[d_rung_var_name].value)
                            if isinstance(value, (int, float)):
                                data[change_var_name].value = value
                                break
                    search -= 1
                if search >= 0:
                    delegate = search

            case TokenType.NEGATIVE:
                dprint('negative')
                d_rung: Token = bureaucracy[delegate]
                match d_rung.t:
                    case TokenType.INT:
                        bureaucracy[delegate].value = - d_rung.value
                    case TokenType.VAR:
                        var_name:str = d_rung.value.name
                        try:
                            var:VariableStruct = data[var_name]
                        except KeyError:
                            continue
                        value = init_rand(var.value)
                        if isinstance(value, (int, float)):
                            data[var_name].value = -value

            case TokenType.OPERATE:
                dprint('operate')
                b = bureaucracy[delegate]
                a = bureaucracy[delegate + 1]
                result = op(a, b)
                if result is None:
                    continue
                b_var: VariableToken = b.value
                b_name = b_var.name
                data[b_name].value = result

            case TokenType.PUNC:
                dprint('punc')
                data_tmp: typing.List[Token] = []
                bureaucrat += 1
                rung: Token = bureaucracy[bureaucrat]
                var: VariableToken = rung.value
                var_name: str = var.name
                var_type = var.init_element
                bureaucrat += 1
                rung: Token = bureaucracy[bureaucrat]
                while rung.t != TokenType.PUNC:
                    data_tmp.append(rung)
                    bureaucrat += 1
                    rung: Token = bureaucracy[bureaucrat]
                if len(data_tmp) == 1:
                    if data_tmp[0].t == TokenType.INT:
                        data_tmp = data_tmp[0].value
                data[var_name] = VariableStruct(data_tmp, var_type)

            case TokenType.INT:
                dprint('int literal')

            case TokenType.VAR:
                dprint('var literal')
                var_name:str = rung.value.name
                if var_name not in data:
                    continue
                var:VariableStruct = data[var_name]
                value:typing.Any = init_rand(var.value)
                if isinstance(value, (int, float)):
                    pass
                elif isinstance(value, list):
                    run(value, debug)
