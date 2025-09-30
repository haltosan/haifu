from math import ceil, floor
from enum import Enum
import typing
# TODO use typing hints properly on everything
# TODO use docstrings
# TODO formatting

#TODO use enums for tokens instead of strings
# double check the changes actually did something

#TODO make structs for variables instead of strings

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


class Token:
    t:TokenType = None
    value = None

    def __init__(self, t, value=None):
        self.t = t
        self.value = value


class VariableToken:
    name:str = None
    init_element = None

    def __init__(self, name, init_element='earth'):
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
        return x
    if x > 0:
        return ceil(x)
    return floor(x)

def yin_or_yang(x) -> int:
    x = strive_num(x)
    return YIN if x % 2 == 0 else YANG

# TODO use enums for elements instead of strings
def element_relationship(element_a, element_b=None, relationship_type=None):
    create_relationship = {
        'earth': 'metal',
        'metal': 'water',
        'water': 'wood',
        'wood': 'fire',
        'fire': 'earth'
    }
    destroy_relationship = {
        'earth': 'water',
        'water': 'fire',
        'fire': 'metal',
        'metal': 'wood',
        'wood': 'earth'
    }
    love_relationship = {
        'earth': 'fire',
        'fire': 'wood',
        'wood': 'water',
        'water': 'metal',
        'metal': 'earth'
    }
    fear_relationship = {
        'earth': 'wood',
        'wood': 'metal',
        'metal': 'fire',
        'fire': 'water',
        'water': 'earth'
    }
    relationship = {
        'create':create_relationship,
        'destroy':destroy_relationship,
        'love':love_relationship,
        'fear':fear_relationship
    }

    a_b_relationship = {(a,relationship[t][a]):t for t in relationship for a in relationship[t]}

    if element_b is None:
        return relationship[relationship_type][element_a]
    return a_b_relationship[element_a, element_b]

def run(bureaucracy, debug=False):
    """expect program of form [lowest, ... highest]"""
    global data

    bureaucrat = 0
    delegate = 0
    def dprint(txt):
        if debug:
            print('\t', txt)

    while bureaucrat < len(bureaucracy):
        rung:Token = bureaucracy[bureaucrat]
        match rung.t:
            case TokenType.HEAVEN:
                dprint('halt')
                return
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
                        if isinstance(value, (int, float)):
                            diff = strive_num(value)
                delegate += diff * sign

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
                        if isinstance(value, (int, float)):
                            diff = strive_num(value)
                bureaucrat += diff * sign

            case TokenType.COUNT | TokenType.SPEAK:
                dprint('print')
                if rung.t == TokenType.SPEAK:
                    def cast(x):
                        return chr(x)
                else:
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

            case TokenType.PUNC:
                dprint('punc')
                data_tmp: typing.List[Token] = []
                bureaucrat += 1
                rung:Token = bureaucracy[bureaucrat]
                var:VariableToken = rung.value
                var_name:str = var.name
                var_type = var.init_element
                bureaucrat += 1
                rung:Token = bureaucracy[bureaucrat]
                while rung.t != TokenType.PUNC:
                    data_tmp.append(rung)
                    bureaucrat += 1
                    rung:Token = bureaucracy[bureaucrat]
                if len(data_tmp) == 1:
                    if data_tmp[0].t == TokenType.INT:
                        data_tmp = data_tmp[0].value
                data[var_name] = VariableStruct(data_tmp, var_type)

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

            case TokenType.INT:
                dprint('int literal')

            case TokenType.VAR:
                dprint('var literal')
                #TODO implement

            case _:
                dprint("other")

        if delegate < 0:
            delegate = 0
        if bureaucrat < 0:
            bureaucrat = 0
        if delegate > bureaucrat:
            delegate = bureaucrat
        if bureaucrat >= len(bureaucracy):
            return
        bureaucrat += 1

def op(a:Token, b:Token) -> typing.Optional[typing.Union[float, int]]:
    global data
    a_name:str = a.value.name
    b_name:str = b.value.name
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
        case 'create':
            return a_val + b_val
        case 'destroy':
            return a_val - b_val
        case 'fear':
            return a_val / b_val
        case 'love':
            return a_val * b_val
        case _:
            if yin_or_yang(a_val) == YANG and yin_or_yang(b_val) == YANG:
                return YANG
            return YIN

if __name__ == '__main__':
    just_exit = [Token(TokenType.HEAVEN)]
    print_123 = [Token(TokenType.INT, 1), Token(TokenType.INT, 2), Token(TokenType.INT, 3),
                 Token(TokenType.COUNT), Token(TokenType.RISE),
                 Token(TokenType.COUNT), Token(TokenType.RISE),
                 Token(TokenType.COUNT), Token(TokenType.HEAVEN)]
    math = [Token(TokenType.PUNC), Token(TokenType.VAR, VariableToken('v1', 'earth')),
            Token(TokenType.INT, 1), Token(TokenType.PUNC),
            Token(TokenType.PUNC), Token(TokenType.VAR, VariableToken('v2', 'metal')),
            Token(TokenType.INT, 2), Token(TokenType.PUNC),
            Token(TokenType.PUNC), Token(TokenType.VAR, VariableToken('v3', 'wood')),
            Token(TokenType.INT, 3), Token(TokenType.PUNC),
            Token(TokenType.PUNC), Token(TokenType.VAR, VariableToken('v4', 'metal')),
            Token(TokenType.INT, 4), Token(TokenType.PUNC),
            Token(TokenType.PUNC), Token(TokenType.VAR, VariableToken('v5', 'earth')),
            Token(TokenType.INT, 5), Token(TokenType.PUNC),
            Token(TokenType.VAR, VariableToken('v1')), Token(TokenType.VAR, VariableToken('v2')),
            Token(TokenType.VAR, VariableToken('v3')), Token(TokenType.VAR, VariableToken('v4')),
            Token(TokenType.VAR, VariableToken('v5')),
            Token(TokenType.INT, 20),
            Token(TokenType.RISE), Token(TokenType.OPERATE), Token(TokenType.COUNT),  # v1
            Token(TokenType.RISE), Token(TokenType.OPERATE), Token(TokenType.COUNT),  # v2
            Token(TokenType.RISE), Token(TokenType.OPERATE), Token(TokenType.COUNT),  # v3
            Token(TokenType.RISE), Token(TokenType.OPERATE), Token(TokenType.COUNT),  # v4
            Token(TokenType.HEAVEN)]
    hello_world = [Token(TokenType.INT, 104), Token(TokenType.INT, 101), Token(TokenType.INT, 108),
                   Token(TokenType.INT, 111), Token(TokenType.INT, 32),
                   Token(TokenType.INT, 119), Token(TokenType.INT, 111), Token(TokenType.INT, 114),
                   Token(TokenType.INT, 108), Token(TokenType.INT, 100), Token(TokenType.INT, 10),
                   Token(TokenType.SPEAK), Token(TokenType.RISE),  # h
                   Token(TokenType.SPEAK), Token(TokenType.RISE),  # e
                   Token(TokenType.SPEAK), Token(TokenType.SPEAK), Token(TokenType.RISE),  # ll
                   Token(TokenType.SPEAK), Token(TokenType.RISE),  # o
                   Token(TokenType.SPEAK), Token(TokenType.RISE),
                   Token(TokenType.SPEAK), Token(TokenType.RISE),  # w
                   Token(TokenType.SPEAK), Token(TokenType.RISE),  # o
                   Token(TokenType.SPEAK), Token(TokenType.RISE),  # r
                   Token(TokenType.SPEAK), Token(TokenType.RISE),  # l
                   Token(TokenType.SPEAK), Token(TokenType.RISE),  # d
                   Token(TokenType.SPEAK), Token(TokenType.RISE),  # \n
                   ]
    loop = [Token(TokenType.INT, 1),  # print val
            Token(TokenType.INT, 4),  # loop jump back
            Token(TokenType.FALL),
            Token(TokenType.COUNT),
            Token(TokenType.RISE),
            Token(TokenType.DEMOTE)]
    programs = [just_exit, print_123, math, hello_world]
    #programs = [loop]

    for p in programs:
        print('--------------')
        run(p, debug=True)
