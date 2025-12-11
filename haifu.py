"""
The main entry point for the project

Error codes:
0 - success
1 - improper argument format
2 - input file does not exist
3 - syntax error
"""

import sys

import parse
import interpret


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage:\n', sys.argv[0], 'file_name', '[debug=0|1]')
        exit(1)
    file_name = sys.argv[1]
    debug = False
    if len(sys.argv) > 2:
        debug = sys.argv[2]
        if debug == '0':
            debug = False
        elif debug == '1':
            debug = True
        else:
            print('Improper argument format', sys.argv)
            print('Expected a \'0\' or \'1\' for debug')
            exit(1)

    try:
        program = parse.parse(file_name)
    except FileNotFoundError:
        print('Input file does not exist')
        exit(2)
    except SyntaxError as e:
        print('Syntax error', e.msg)
        exit(3)

    interpret.run(program, debug=debug)