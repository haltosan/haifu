from math import ceil, floor
from enum import Enum
#TODO use enums for tokens instead of strings
# double check the changes actually did something

data = dict()
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


def strive(x):
    #TODO incomplete
    if x > 0:
        return ceil(x)
    return floor(x)

def yin_or_yang(x) -> int:
    if type(x) is float:
        x = strive(x)
    return YIN if x % 2 == 0 else YANG

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
                match lower.t:
                    case TokenType.INT:
                        delegate += lower.value * sign
                    case TokenType.VAR:
                        #TODO implement
                        pass
                    case _:
                        delegate += 1 * sign
                # elif ' ' in lower:
                #     var_name = lower.split(' ')[0]
                #     var_data = data[var_name][1]
                #     if type(var_data) is int:
                #         delegate += var_data * sign

                if delegate < 0:  # TODO move clamping to end of loop
                    delegate = 0
                elif delegate > bureaucrat:
                    delegate = bureaucrat
                continue

            case TokenType.PROMOTE | TokenType.DEMOTE:
                dprint('promote/demote')
                if rung.t == TokenType.DEMOTE:
                    sign = -1
                else:
                    sign = 1
                d_rung:Token = bureaucracy[delegate]
                diff = 0
                match d_rung.t:
                    case TokenType.INT:
                        diff = d_rung
                    case TokenType.VAR:
                        #TODO implement
                        diff = 0
                        # var_name = d_rung.split(' ')[0]
                        # var_data = data[var_name][1]
                        # if type(var_data) is int:
                        #     diff = var_data
                        # else:
                        #     diff = 0
                    case _:
                        diff = 0
                bureaucrat += diff * sign  # TODO make consistent

                if bureaucrat < 0:
                    bureaucrat = 0
                elif bureaucrat >= len(bureaucracy):
                    return

                if delegate > bureaucrat:
                    delegate = bureaucrat

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
                        # TODO implement
                        pass
                # elif ' ' in d_rung:
                #     print(data[d_rung.split(' ')[0]][1], end='')

            case TokenType.PUNC:
                dprint('punc')
                data_tmp = []
                bureaucrat += 1
                # TODO redo with new var structure
                var_name, var_type = bureaucracy[bureaucrat].split(' ')
                bureaucrat += 1
                while (rung := bureaucracy[bureaucrat]) not in ['/', var_name]:
                    data_tmp.append(rung)
                    bureaucrat += 1
                if len(data_tmp) == 1:
                    data_tmp = data_tmp[0]
                data[var_name] = [var_type, data_tmp]

            case TokenType.OPERATE:
                dprint('operate')
                b = bureaucracy[delegate]
                a = bureaucracy[delegate + 1]
                result = op(a, b)
                #TODO new var structure
                b_name = b.split(' ')[0]
                data[b_name][1] = result

            case TokenType.INT:
                dprint('int literal')

            case TokenType.VAR:
                dprint('var literal')
                #TODO implement

            case _:
                dprint("other")

        bureaucrat += 1

def op(a, b):
    global data
    a_name = a.split(' ')[0]
    b_name = b.split(' ')[0]
    a_type, a_val = data[a_name]
    if not isinstance(a_val, (int, float)):
        return None
    b_type, b_val = data[b_name]
    if not isinstance(b_val, (int, float)):
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
    math = [Token(TokenType.PUNC), Token(TokenType.VAR, 'v1 earth'),
            Token(TokenType.INT, 1), Token(TokenType.PUNC),
            Token(TokenType.PUNC), Token(TokenType.VAR, 'v2 metal'),
            Token(TokenType.INT, 2), Token(TokenType.PUNC),
            Token(TokenType.PUNC), Token(TokenType.VAR, 'v3 wood'),
            Token(TokenType.INT, 3), Token(TokenType.PUNC),
            Token(TokenType.PUNC), Token(TokenType.VAR, 'v4 metal'),
            Token(TokenType.INT, 4), Token(TokenType.PUNC),
            Token(TokenType.PUNC), Token(TokenType.VAR, 'v5 earth'),
            Token(TokenType.INT, 5), Token(TokenType.PUNC),
            Token(TokenType.VAR, 'v1 earth'), Token(TokenType.VAR, 'v2 metal'),
            Token(TokenType.VAR, 'v3 wood'), Token(TokenType.VAR, 'v4 metal'),
            Token(TokenType.VAR, 'v5 earth'),
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
                   Token(TokenType.SPEAK), Token(TokenType.RISE), Token(TokenType.RISE),  # ll
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
    #programs = [just_exit, print_123, math]
    programs = [loop]

    for p in programs:
        print('--------------')
        run(p, debug=True)
