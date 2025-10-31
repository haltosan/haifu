import pytest

from interpret import *

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
blossom_loop = [Token(TokenType.PUNC),
                Token(TokenType.VAR, VariableToken('v1', ElementType.EARTH)),
                Token(TokenType.INT, 2),
                Token(TokenType.PUNC),
                Token(TokenType.PUNC),
                Token(TokenType.VAR, VariableToken('v2', ElementType.EARTH)),
                Token(TokenType.COUNT),
                Token(TokenType.PUNC),
                Token(TokenType.INT, 1),
                Token(TokenType.VAR, VariableToken('v1')),
                Token(TokenType.VAR, VariableToken('v2')),
                # data end
                Token(TokenType.OPERATE),
                Token(TokenType.INT, 8),
                Token(TokenType.RISE),
                Token(TokenType.BLOSSOM),
                Token(TokenType.COUNT),
                Token(TokenType.RISE),
                Token(TokenType.BLOSSOM),
                Token(TokenType.RISE),
                Token(TokenType.BLOSSOM)]

element_changes = [Token(TokenType.PUNC),
                   Token(TokenType.VAR, VariableToken('b', ElementType.METAL)),
                   Token(TokenType.INT, 3),
                   Token(TokenType.PUNC),
                   Token(TokenType.PUNC),
                   Token(TokenType.VAR, VariableToken('a', ElementType.EARTH)),
                   Token(TokenType.INT, 2),
                   Token(TokenType.PUNC),
                   Token(TokenType.VAR, VariableToken('b')),
                   Token(TokenType.VAR, VariableToken('a')),
                   Token(TokenType.INT, 8),
                   Token(TokenType.RISE),
                   Token(TokenType.CREATE),
                   Token(TokenType.DESTROY),
                   Token(TokenType.LOVE),
                   Token(TokenType.FEAR),
                   Token(TokenType.OPERATE),
                   Token(TokenType.COUNT)]

become_1 = [Token(TokenType.INT, 1),
            Token(TokenType.BECOME),
            Token(TokenType.COUNT),
            Token(TokenType.INT, 0),
            Token(TokenType.INT, 6),
            Token(TokenType.INT, 3),
            Token(TokenType.RISE),
            Token(TokenType.BECOME),
            Token(TokenType.RISE),
            Token(TokenType.DEMOTE),
            Token(TokenType.COUNT)]

become_2 = [Token(TokenType.PUNC),
            Token(TokenType.VAR, VariableToken('non-zero')),
            Token(TokenType.INT, 1),
            Token(TokenType.PUNC),
            Token(TokenType.PUNC),
            Token(TokenType.VAR, VariableToken('zero')),
            Token(TokenType.INT, 0),
            Token(TokenType.PUNC),
            Token(TokenType.VAR, VariableToken('non-zero')),
            Token(TokenType.VAR, VariableToken('zero')),
            Token(TokenType.INT, 9),
            Token(TokenType.INT, 8),
            Token(TokenType.RISE),
            Token(TokenType.BECOME),
            Token(TokenType.COUNT),
            Token(TokenType.RISE),
            Token(TokenType.BECOME),
            Token(TokenType.RISE),
            Token(TokenType.DEMOTE),
            Token(TokenType.COUNT)]

negative = [Token(TokenType.INT, 1),
          Token(TokenType.NEGATIVE),
          Token(TokenType.COUNT),
          Token(TokenType.PUNC),
          Token(TokenType.VAR, VariableToken('one')),
          Token(TokenType.INT, 1),
          Token(TokenType.PUNC),
          Token(TokenType.PUNC),
          Token(TokenType.VAR, VariableToken('halt')),
          Token(TokenType.HEAVEN),
          Token(TokenType.PUNC),
          Token(TokenType.INT, 4),
          Token(TokenType.RISE),
          Token(TokenType.NEGATIVE),
          Token(TokenType.COUNT),
          Token(TokenType.INT, 4),
          Token(TokenType.RISE),
          Token(TokenType.NEGATIVE),
          Token(TokenType.COUNT)]

like = [Token(TokenType.COUNT),
        Token(TokenType.LIKE),
        Token(TokenType.INT, 1),
        Token(TokenType.PUNC),
        Token(TokenType.VAR, VariableToken('two')),
        Token(TokenType.INT, 2),
        Token(TokenType.PUNC),
        Token(TokenType.PUNC),
        Token(TokenType.VAR, VariableToken('dest')),
        Token(TokenType.INT, 0),
        Token(TokenType.PUNC),
        Token(TokenType.INT, 3),
        Token(TokenType.RISE),
        Token(TokenType.VAR, VariableToken('dest')),
        Token(TokenType.LIKE),
        Token(TokenType.INT, 6),
        Token(TokenType.RISE),
        Token(TokenType.COUNT),
        Token(TokenType.INT, 4),
        Token(TokenType.FALL),
        Token(TokenType.VAR, VariableToken('dest')),
        Token(TokenType.LIKE),
        Token(TokenType.INT, 4),
        Token(TokenType.RISE),
        Token(TokenType.COUNT)]

bureaucrat_control = [Token(TokenType.INT, 2),
                      Token(TokenType.INT, 0),
                      Token(TokenType.INT, 0),
                      Token(TokenType.PUNC),
                      Token(TokenType.VAR, VariableToken('num')),
                      Token(TokenType.INT, 4),
                      Token(TokenType.PUNC),
                      Token(TokenType.PUNC),
                      Token(TokenType.VAR, VariableToken('non-num')),
                      Token(TokenType.HEAVEN),
                      Token(TokenType.PUNC),
                      Token(TokenType.PROMOTE),
                      Token(TokenType.COUNT),
                      Token(TokenType.COUNT),
                      Token(TokenType.INT, 4),
                      Token(TokenType.RISE),
                      Token(TokenType.DEMOTE),
                      Token(TokenType.DEMOTE)]

# TODO 100% line coverage

class TestRun:

    @pytest.fixture(scope='function', autouse=True)
    def debug_on_fail(self, request):
        yield
        if request.session.testsfailed:
            return '#####################################################'

    def test_run_just_exit(self, capsys):
        run(just_exit, debug=True)
        out, err = capsys.readouterr()
        assert out == '', err

    def test_run_print_123(self, capsys, debug_on_fail):
        run(print_123, debug=True)
        out, err = capsys.readouterr()
        assert out == '123', err

    def test_run_math(self, capsys):
        run(math, debug=True)
        out, err = capsys.readouterr()
        assert out == '311.333333333333333320', err

    def test_run_hello_world(self, capsys):
        run(hello_world, debug=True)
        out, err = capsys.readouterr()
        assert out == 'hello world\n', err

    def test_run_print_function(self, capsys):
        run(print_function, debug=True)
        out, err = capsys.readouterr()
        assert out == '111', err

    def test_run_blossom_loop(self, capsys):
        run(blossom_loop, debug=True)
        out, err = capsys.readouterr()
        assert out == '12', err

    def test_run_element_change(self, capsys):
        run(element_changes, debug=True)
        out, err = capsys.readouterr()
        assert out == '6', err

    def test_run_become(self, capsys):
        run(become_1, debug=True)
        out, err = capsys.readouterr()
        assert out == '2', err
        run(become_2, debug=True)
        out, err = capsys.readouterr()
        assert out == '2', err

    def test_run_negative(self, capsys):
        run(negative, debug=True)
        out, err = capsys.readouterr()
        assert out == '-1-1', err

    def test_run_like(self, capsys):
        run(like, debug=True)
        out, err = capsys.readouterr()
        assert out == '12', err

    def test_run_bureaucrat_control(self, capsys):
        run(bureaucrat_control, debug=True)
        out, err = capsys.readouterr()
        assert out == '244', err