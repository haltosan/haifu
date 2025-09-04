data = dict()
#TODO get element relationship table
element_relationship = dict()

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
            delegate += 1
        elif rung in ['count', 'number', 'age']:
            dprint('number')
            if type(bureaucracy[delegate]) is int:
                print(bureaucracy[delegate])
        elif rung == '/':
            dprint('punc')
            data_tmp = []
            bureaucrat += 1
            var_name, var_type = bureaucracy[bureaucrat].split(' ')
            bureaucrat += 1
            while (rung := bureaucracy[bureaucrat]) not in ['/', var_name]:
                data_tmp.append(rung)
                bureaucrat += 1
            bureaucrat += 1
            if len(data_tmp) == 1:
                data_tmp = data_tmp[0]
            data[var_name] = [var_type, data_tmp]
        elif rung in ['operate', 'examine', 'study']:
            b = bureaucracy[delegate]
            a = bureaucracy[delegate + 1]

        elif ' ' in rung:  # variable
            dprint('var literal')
            #TODO implement
            pass
        elif type(rung) is int:
            dprint('int literal')
            pass
        else:
            dprint('other')
            pass
        bureaucrat += 1

def op(a, b):
    global data
    a_name, a_type = a.split(' ')
    b_name, b_type = b.split(' ')
    match element_relationship[b_type, a_type]:
        case 'creates':
            '+'
        case 'destroys':
            '-'
        case 'fears':
            '/'
        case 'loves':
            '*'
        case _:
            'yin/yang'
        #TODO finish

if __name__ == '__main__':
    just_exit = ['nirvana']
    print_123 = [1, 2, 3, 'number', 'up', 'number', 'up', 'number', 'heaven']
    math = ['/', 'v1 earth', 1, '/', '/', 'v2 metal', 2, '/', '/', 'v3 wood', 3, '/', '/', 'v4 metal', 4, '/', '/', 'v5 earth', '/'
            'v1 earth', 'v2 metal', 'v3 wood', 'v4 metal', 'v5 earth',
            23,
            'up', 'study', 'age',  # v1
            'up', 'study', 'age',  # v2
            'up', 'study', 'age',  # v3
            'up', 'study', 'age',  # v4
            'up', 'study', 'age',  # v5
            'nirvana']
    #programs = [just_exit, print_123, math]
    programs = [math]

    for p in programs:
        print('--------------')
        run(p, debug=True)
