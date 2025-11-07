import interpret
from interpret import Token, TokenType, VariableToken, ElementType

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
blossom_loop = [Token(TokenType.VAR, VariableToken('bogus')),
                Token(TokenType.BLOSSOM),
                Token(TokenType.INT, 4),
                Token(TokenType.RISE),
                Token(TokenType.PUNC),
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

element_changes = [Token(TokenType.VAR, VariableToken('bogus')),
                   Token(TokenType.CREATE),
                   Token(TokenType.COUNT),
                   Token(TokenType.INT, 2),
                   Token(TokenType.RISE),
                   Token(TokenType.CREATE),
                   Token(TokenType.INT, 7),
                   Token(TokenType.RISE),
                   Token(TokenType.PUNC),
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

become_1 = [Token(TokenType.INT, -1),
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

become_2 = [Token(TokenType.VAR, VariableToken('bogus')),
            Token(TokenType.BECOME),
            Token(TokenType.INT, 4),
            Token(TokenType.RISE),
            Token(TokenType.PUNC),
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

negative = [Token(TokenType.VAR, VariableToken('bogus')),
            Token(TokenType.NEGATIVE),
            Token(TokenType.INT,4),
            Token(TokenType.RISE),
            Token(TokenType.INT, 1),
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

like = [Token(TokenType.VAR, VariableToken('bogus')),
        Token(TokenType.LIKE),
        Token(TokenType.INT, 4),
        Token(TokenType.RISE),
        Token(TokenType.COUNT),
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

bureaucrat_control = [Token(TokenType.VAR, VariableToken('bogus')),
                      Token(TokenType.PROMOTE),
                      Token(TokenType.INT, 4),
                      Token(TokenType.RISE),
                      Token(TokenType.INT, 2),
                      Token(TokenType.VAR, VariableToken('nop')),
                      Token(TokenType.VAR, VariableToken('nop')),
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

delegate_control = [Token(TokenType.VAR, VariableToken('bogus')),
                    Token(TokenType.RISE),
                    Token(TokenType.PUNC),
                    Token(TokenType.VAR, VariableToken('num')),
                    Token(TokenType.INT, 3),
                    Token(TokenType.PUNC),
                    Token(TokenType.PUNC),
                    Token(TokenType.VAR, VariableToken('non-num')),
                    Token(TokenType.VAR, VariableToken('bogus')),
                    Token(TokenType.PUNC),
                    Token(TokenType.VAR, VariableToken('num')),
                    Token(TokenType.RISE),
                    Token(TokenType.COUNT),
                    Token(TokenType.VAR, VariableToken('non-num')),
                    Token(TokenType.RISE),
                    Token(TokenType.COUNT)]

clamping = [Token(TokenType.VAR, VariableToken('var')),
            Token(TokenType.INT, 15),
            Token(TokenType.PROMOTE),
            Token(TokenType.PUNC),
            Token(TokenType.VAR, VariableToken('var')),
            Token(TokenType.INT, 16),
            Token(TokenType.PUNC),
            Token(TokenType.INT, 5),
            Token(TokenType.FALL),
            Token(TokenType.RISE),
            Token(TokenType.DEMOTE)]


class TestRun:
    def test_run_just_exit(self, capsys):
        interpret.run(just_exit, debug=True)
        out, err = capsys.readouterr()
        assert out == '', err

    def test_run_print_123(self, capsys):
        interpret.run(print_123, debug=True)
        out, err = capsys.readouterr()
        assert out == '123', err

    def test_run_math(self, capsys):
        interpret.run(math, debug=True)
        out, err = capsys.readouterr()
        assert out == '311.333333333333333320', err

    def test_run_hello_world(self, capsys):
        interpret.run(hello_world, debug=True)
        out, err = capsys.readouterr()
        assert out == 'hello world\n', err

    def test_run_print_function(self, capsys):
        interpret.run(print_function, debug=True)
        out, err = capsys.readouterr()
        assert out == '111', err

    def test_run_blossom_loop(self, capsys):
        interpret.run(blossom_loop, debug=True)
        out, err = capsys.readouterr()
        assert out == '12', err

    def test_run_element_change(self, capsys):
        interpret.run(element_changes, debug=True)
        out, err = capsys.readouterr()
        assert out == '6', err

    def test_run_become(self, capsys):
        interpret.run(become_1, debug=True)
        out, err = capsys.readouterr()
        assert out == '-2', err
        interpret.run(become_2, debug=True)
        out, err = capsys.readouterr()
        assert out == '2', err

    def test_run_negative(self, capsys):
        interpret.run(negative, debug=True)
        out, err = capsys.readouterr()
        assert out == '-1-1', err

    def test_run_like(self, capsys):
        interpret.run(like, debug=True)
        out, err = capsys.readouterr()
        assert out == '12', err

    def test_run_bureaucrat_control(self, capsys):
        interpret.run(bureaucrat_control, debug=True)
        out, err = capsys.readouterr()
        assert out == '244', err

    def test_run_delegate_control(self, capsys):
        interpret.run(delegate_control, debug=True)
        out, err = capsys.readouterr()
        assert out == '33', err

    def test_run_clamping(self, capsys):
        interpret.run(clamping, debug=True)
        out, err = capsys.readouterr()
        assert out == '', err

    def test_run_listen(self, capsys):
        try:
            interpret.run([Token(TokenType.LISTEN)], debug=True)
            _, err = capsys.readouterr()
            assert False, err
        except NotImplementedError:
            assert True


class TestInternal:
    def test_strive_num(self):
        assert interpret.strive_num(1.1) == 2
        assert interpret.strive_num(-2.9) == -3

    def test_yin_or_yang(self):
        assert interpret.yin_or_yang('non-num') is None
        assert interpret.yin_or_yang(1.2) == interpret.YIN

    def test_op(self):
        interpret.data['a'] = interpret.VariableStruct(None, ElementType.EARTH)
        interpret.data['b'] = interpret.VariableStruct(1, ElementType.EARTH)
        interpret.data['c'] = interpret.VariableStruct(2, ElementType.EARTH)
        assert interpret.op(Token(TokenType.VAR, VariableToken('bogus')),
                            Token(TokenType.VAR, VariableToken('bogus'))) is None
        assert interpret.op(Token(TokenType.VAR, VariableToken('a')),
                            Token(TokenType.VAR, VariableToken('bogus'))) is None
        assert interpret.op(Token(TokenType.VAR, VariableToken('b')),
                            Token(TokenType.VAR, VariableToken('bogus'))) is None
        assert interpret.op(Token(TokenType.VAR, VariableToken('b')),
                            Token(TokenType.VAR, VariableToken('a'))) is None
        assert interpret.op(Token(TokenType.VAR, VariableToken('b')),
                            Token(TokenType.VAR, VariableToken('b'))) is interpret.YANG
        assert interpret.op(Token(TokenType.VAR, VariableToken('b')),
                            Token(TokenType.VAR, VariableToken('c'))) is interpret.YIN

    def test_rand(self):
        a = interpret.init_rand(Token(TokenType.RAND))
        b = interpret.init_rand(Token(TokenType.RAND))
        assert a != b, 'Random values likely are not the same'
