from math import ceil, floor

data = dict()

YIN = 2
YANG = 1

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
        rung = bureaucracy[bureaucrat]
        if rung in ['heaven', 'nirvana', 'enlightenment', 'harmony']:
            dprint('halt')
            return

        elif rung in ['rise', 'float', 'ascend', 'up']:
            dprint('up')
            lower = bureaucracy[bureaucrat - 1]
            if type(lower) is int:
                delegate += lower
            elif ' ' in lower:
                var_name = lower.split(' ')[0]
                var_data = data[var_name][1]
                if type(var_data) is int:
                    delegate += var_data
            else:
                delegate += 1

        elif rung in ['count', 'number', 'age']:
            dprint('number')
            d_rung = bureaucracy[delegate]
            if type(d_rung) is int:
                print(d_rung, end='')
            elif ' ' in d_rung:
                print(data[d_rung.split(' ')[0]][1], end='')

        elif rung in ['speak', 'say', 'draw']:
            dprint('say')
            d_rung = bureaucracy[delegate]
            if type(d_rung) is int:
                print(chr(d_rung), end='')
            elif ' ' in d_rung:
                print(chr(data[d_rung.split(' ')[0][1]]), end='')

        elif rung == '/':
            dprint('punc')
            data_tmp = []
            bureaucrat += 1
            var_name, var_type = bureaucracy[bureaucrat].split(' ')
            bureaucrat += 1
            while (rung := bureaucracy[bureaucrat]) not in ['/', var_name]:
                data_tmp.append(rung)
                bureaucrat += 1
            if len(data_tmp) == 1:
                data_tmp = data_tmp[0]
            data[var_name] = [var_type, data_tmp]

        elif rung in ['operate', 'examine', 'study']:
            dprint('operate')
            b = bureaucracy[delegate]
            a = bureaucracy[delegate + 1]
            result = op(a, b)
            b_name = b.split(' ')[0]
            data[b_name][1] = result

        elif type(rung) is int:
            dprint('int literal')
            pass

        elif ' ' in rung:  # variable
            dprint('var literal')
            #TODO implement
            pass

        else:
            dprint('other')
            pass

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
    just_exit = ['nirvana']
    print_123 = [1, 2, 3, 'number', 'up', 'number', 'up', 'number', 'heaven']
    math = ['/', 'v1 earth', 1, '/', '/', 'v2 metal', 2, '/', '/', 'v3 wood', 3, '/', '/', 'v4 metal', 4, '/', '/', 'v5 earth', 5, '/',
            'v1 earth', 'v2 metal', 'v3 wood', 'v4 metal', 'v5 earth',
            20,
            'up', 'study', 'age',  # v1
            'up', 'study', 'age',  # v2
            'up', 'study', 'age',  # v3
            'up', 'study', 'age',  # v4
            'nirvana']
    hello_world = [104, 101, 108, 111, 32,
                   119, 111, 114, 108, 100, 10,
                   'say', 'up',  # h
                   'say', 'up',  # e
                   'say', 'say', 'up',  # ll
                   'say', 'up',  # o
                   'say', 'up',
                   'say', 'up',  # w
                   'say', 'up',  # o
                   'say', 'up',  # r
                   'say', 'up',  # l
                   'say', 'up',  # d
                   'say', 'up',  # \n
                   ]
    #programs = [just_exit, print_123, math]
    programs = [hello_world]

    for p in programs:
        print('--------------')
        run(p, debug=True)
