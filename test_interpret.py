from interpret import *
import pytest

just_exit = [Token(TokenType.HEAVEN)]
print_123 = [Token(TokenType.INT, 1), Token(TokenType.INT, 2), Token(TokenType.INT, 3),
             Token(TokenType.COUNT), Token(TokenType.RISE),
             Token(TokenType.COUNT), Token(TokenType.RISE),
             Token(TokenType.COUNT), Token(TokenType.HEAVEN)]
math = [Token(TokenType.PUNC), Token(TokenType.VAR, VariableToken('v1', ElementType.EARTH)),
        Token(TokenType.INT, 1), Token(TokenType.PUNC),
        Token(TokenType.PUNC), Token(TokenType.VAR, VariableToken('v2', ElementType.METAL)),
        Token(TokenType.INT, 2), Token(TokenType.PUNC),
        Token(TokenType.PUNC), Token(TokenType.VAR, VariableToken('v3', ElementType.WOOD)),
        Token(TokenType.INT, 3), Token(TokenType.PUNC),
        Token(TokenType.PUNC), Token(TokenType.VAR, VariableToken('v4', ElementType.METAL)),
        Token(TokenType.INT, 4), Token(TokenType.PUNC),
        Token(TokenType.PUNC), Token(TokenType.VAR, VariableToken('v5', ElementType.EARTH)),
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
print_function = [Token(TokenType.PUNC),
                  Token(TokenType.VAR, VariableToken('print')),
                  Token(TokenType.INT, 1), Token(TokenType.COUNT), Token(TokenType.HEAVEN),
                  Token(TokenType.PUNC),
                  Token(TokenType.VAR, VariableToken('print')),
                  Token(TokenType.VAR, VariableToken('print')),
                  Token(TokenType.VAR, VariableToken('print'))]
# TODO test including new instructions: blossom, listen, create/destroy/fear/love, become

def test_run_just_exit(capsys):
    run(just_exit, debug=True)
    out, _ = capsys.readouterr()
    assert out == ''

def test_run_print_123(capsys):
    run(print_123, debug=True)
    out, _ = capsys.readouterr()
    assert out == '123'

def test_run_math(capsys):
    run(math, debug=True)
    out, _ = capsys.readouterr()
    assert out == '311.333333333333333320'

def test_run_hello_world(capsys):
    run(hello_world, debug=True)
    out, _ = capsys.readouterr()
    assert out == 'hello world\n'

def test_run_print_function(capsys):
    run(print_function, debug=True)
    out, _ = capsys.readouterr()
    assert out == '111'