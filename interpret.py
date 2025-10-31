from math import ceil, floor
from enum import Enum
import typing
import sys
# TODO use typing hints properly on everything
# TODO use docstrings
# TODO formatting

YIN = 2
YANG = 1


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


class ElementType(Enum):
    WOOD = 0
    FIRE = 1
    EARTH = 2
    METAL = 3
    WATER = 4


class ElementRelationship(Enum):
    CREATE = 0
    DESTROY = 1
    FEAR = 2
    LOVE = 3
    SAME = 4

class Token:
    t:TokenType = None
    value:typing.Any = None

    def __init__(self, t, value=None):
        self.t = t
        self.value = value


class VariableToken:
    name:str = None
    init_element:ElementType = None

    def __init__(self, name, init_element:ElementType=ElementType.EARTH):
        self.name = name
        self.init_element = init_element


class VariableStruct:
    element = None
    value = None

    def __init__(self, value, element):
        self.element = element
        self.value = value


data: typing.Dict[str, VariableStruct] = dict()

def strive_num(x: typing.Union[int, float]) -> int:
    if type(x) is int:
        if x < 0:
            return x - 1
        return x + 1
    if x > 0:
        return ceil(x)
    return floor(x)

def yin_or_yang(x) -> typing.Optional[int]:
    if not isinstance(x, (int, float)):
        return None
    if type(x) is float:
        x = strive_num(x)
    return YIN if x % 2 == 0 else YANG

def element_relationship(element_a:ElementType, element_b:ElementType=None, relationship_type:ElementRelationship=None) -> typing.Union[ElementType, ElementRelationship]:
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
    return a_b_relationship[element_a, element_b]

def op(a:Token, b:Token) -> typing.Optional[typing.Union[float, int]]:
    global data
    try:
        a_name:str = a.value.name
        b_name:str = b.value.name
    except AttributeError:
        return None
    a_var:VariableStruct = data[a_name]
    a_type = a_var.element
    a_val = a_var.value
    if not isinstance(a_val, (int, float)):
        return None
    b_var = data[b_name]
    b_type = b_var.element
    b_val = b_var.value
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

def run(bureaucracy, debug=False):
    """expect program of form [lowest, ... highest]"""
    global data

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
        rung:Token = bureaucracy[bureaucrat]
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
                d_rung:Token = bureaucracy[delegate]
                diff:int = 0
                match d_rung.t:
                    case TokenType.INT:
                        diff = d_rung.value
                    case TokenType.VAR:
                        var_name:str = d_rung.value.name
                        var:VariableStruct = data[var_name]
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
                        var:VariableStruct = data[var_name]
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

                lower:Token = bureaucracy[bureaucrat - 1]
                diff:int = 1
                match lower.t:
                    case TokenType.INT:
                        diff = lower.value
                    case TokenType.VAR:
                        var_name:str = lower.value.name
                        var:VariableStruct = data[var_name]
                        value = var.value
                        if type(value) is int:
                            diff = value
                        else:
                            continue
                delegate += diff * sign

            case TokenType.LISTEN:
                dprint('listen')
                raise NotImplemented('Higher levels needed')
                # TODO use earlier layers to make it a token
                # TODO how on earth do you detect if there's no stdin????

            case TokenType.COUNT | TokenType.SPEAK:
                if rung.t == TokenType.SPEAK:
                    dprint('speak')
                    def cast(x):
                        return chr(x)
                else:
                    dprint('count')
                    def cast(x):
                        return x

                d_rung:Token = bureaucracy[delegate]
                match d_rung.t:
                    case TokenType.INT:
                        print(cast(d_rung.value), end='')
                    case TokenType.VAR:
                        var_name:str = d_rung.value.name
                        var:VariableStruct = data[var_name]
                        value = var.value
                        if isinstance(value, (int, float)):
                            print(cast(value), end='')

            case TokenType.CREATE | TokenType.DESTROY | TokenType.FEAR | TokenType.LOVE:
                dprint('element change')
                d_rung:Token = bureaucracy[delegate]
                if d_rung.t != TokenType.VAR:
                    continue
                var_name:str = d_rung.value.name
                current_element:ElementType = data[var_name].element
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
                d_rung:Token = bureaucracy[delegate]
                match d_rung.t:
                    case TokenType.INT:
                        value:int = d_rung.value
                        if value == 0:
                            bureaucracy[delegate] = Token(TokenType.HEAVEN)
                        else:
                            bureaucracy[delegate].value = strive_num(value)
                    case TokenType.VAR:
                        var_name:str = d_rung.value.name
                        var:VariableStruct = data[var_name]
                        value = var.value
                        if isinstance(value, (int, float)):
                            if value == 0:
                                bureaucracy[delegate] = Token(TokenType.HEAVEN)
                                continue
                            else:
                                data[var_name].value = strive_num(value)
                            var_type:ElementType = var.element
                            data[var_name].element = element_relationship(element_a=var_type, relationship_type=ElementRelationship.CREATE)

            case TokenType.LIKE:
                dprint('like')
                change:Token = bureaucracy[bureaucrat - 1]
                if change.t != TokenType.VAR:
                    continue
                change_var_name:str = change.value.name
                search:int = delegate
                while search >= 0:
                    d_rung:Token = bureaucracy[search]
                    match d_rung.t:
                        case TokenType.INT:
                            data[change_var_name].value = d_rung.value
                            break
                        case TokenType.VAR:
                            d_rung_var_name:str = d_rung.value.name
                            value = data[d_rung_var_name].value
                            if isinstance(value, (int, float)):
                                data[change_var_name].value = value
                                break
                    search -= 1
                if search >= 0:
                    delegate = search

            case TokenType.NEGATIVE:
                dprint('negative')
                d_rung:Token = bureaucracy[delegate]
                match d_rung.t:
                    case TokenType.INT:
                        bureaucracy[delegate].value = - d_rung.value
                    case TokenType.VAR:
                        var_name:str = d_rung.value.name
                        var:VariableStruct = data[var_name]
                        if isinstance(var.value, (int, float)):
                            data[var_name].value = -var.value

            case TokenType.OPERATE:
                dprint('operate')
                b = bureaucracy[delegate]
                a = bureaucracy[delegate + 1]
                result = op(a, b)
                if result is None:
                    continue
                b_var:VariableToken = b.value
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
                value:typing.Any = var.value
                if isinstance(value, (int, float)):
                    pass
                elif type(value) is list:
                    run(value, debug)
