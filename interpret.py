def run(bureaucracy, debug=False):
    """expect program of form [lowest, ... highest]"""
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
        else:
            dprint('other')
            pass
        bureaucrat += 1



if __name__ == '__main__':
    just_exit = ['nirvana']
    _123 = [1, 2, 3, 'number', 'up', 'number', 'up', 'number', 'heaven']
    programs = [just_exit, _123]

    for p in programs:
        print('--------------')
        run(p, debug=True)
