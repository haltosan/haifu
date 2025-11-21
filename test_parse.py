import pathlib

import pytest

import interpret
import parse


class TestContract:
    class TestParse:
        tmp_file = 'tmp.haifu'

        def write(self, text):
            with open(self.tmp_file, 'w') as file:
                file.write(text)

        def raw_to_out(self, raw):
            self.write(raw)
            return parse.parse(self.tmp_file)

        @pytest.fixture(autouse=True)
        def cleanup(self):
            open(self.tmp_file, 'w').close()

        def test_parse_just_exit(self):
            raw = ('heaven, test test test\n'
                   'longer longer longer test\n'
                   'longer longer test')
            out = self.raw_to_out(raw)
            assert out == [interpret.Token(interpret.TokenType.HEAVEN)], out

        def test_parse_print_123(self):
            raw = ('one two three count rise\n'
                   'count rise count heaven, four test\n'
                   'longer longer test')
            out = self.raw_to_out(raw)
            assert out == [interpret.Token(interpret.TokenType.INT, 1),
                           interpret.Token(interpret.TokenType.INT, 2),
                           interpret.Token(interpret.TokenType.INT, 3),
                           interpret.Token(interpret.TokenType.COUNT),
                           interpret.Token(interpret.TokenType.RISE),
                           interpret.Token(interpret.TokenType.COUNT),
                           interpret.Token(interpret.TokenType.RISE),
                           interpret.Token(interpret.TokenType.COUNT),
                           interpret.Token(interpret.TokenType.HEAVEN)], out

        def test_print_var_elements(self):
            raw = ('tree flame metal ice\n'
                   'soil spirit, and pumpkin spice\n'
                   'longer longer test')
            out = self.raw_to_out(raw)
            assert out == [interpret.Token(interpret.TokenType.VAR,
                                           interpret.VariableToken('tree', interpret.ElementType.WOOD)),
                           interpret.Token(interpret.TokenType.VAR,
                                           interpret.VariableToken('flame', interpret.ElementType.FIRE)),
                           interpret.Token(interpret.TokenType.VAR,
                                           interpret.VariableToken('metal', interpret.ElementType.METAL)),
                           interpret.Token(interpret.TokenType.VAR,
                                           interpret.VariableToken('ice', interpret.ElementType.WATER)),
                           interpret.Token(interpret.TokenType.VAR,
                                           interpret.VariableToken('soil', interpret.ElementType.EARTH)),
                           interpret.Token(interpret.TokenType.VAR,
                                           interpret.VariableToken('spirit', interpret.ElementType.EARTH))
                           ], out

    class TestInternals:
        def test_read_file_negative(self):
            file_name = 'nonexist.txt'
            try:
                pathlib.Path(file_name).unlink()
            except FileNotFoundError:
                pass
            assert parse.read_file(file_name) == '', 'Nonexistent files MUST be blank'

        def test_read_file_positive(self):
            file_name = 'full.txt'
            text = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit, '
                    'sed do eiusmod tempor incididunt ut labore et dolore magna '
                    'aliqua. Ut enim ad minim veniam, quis nostrud exercitation '
                    'ullamco laboris nisi ut aliquip ex ea commodo consequat.')
            with open(file_name, 'w') as file:
                file.write(text)
            assert parse.read_file(file_name) == text, 'Text does not match'
            pathlib.Path(file_name).unlink()

        def test_make_stanzas_positive(self):
            text = ('line 1\n'
                    'line 2\n'
                    'line 3\n'
                    '\n'
                    'line 4\n'
                    'line 5\n'
                    'line 6')
            for _ in range(2):
                try:
                    stanzas = parse.make_stanzas(text)
                    assert len(stanzas) == 2
                    assert stanzas[0] == 'line 1\nline 2\nline 3'
                    assert stanzas[1] == 'line 4\nline 5\nline 6'
                except SyntaxError:
                    assert False, '7 lines is valid'
                text += '\n'

            try:
                assert parse.make_stanzas('') == []
            except SyntaxError:
                assert False, '0 lines is valid'

        def test_make_stanzas_negative(self):
            text = ('line 1\n'
                    'line 2')
            try:
                parse.make_stanzas(text)
                assert False, '2 lines is not valid'
            except SyntaxError:
                pass

            text += ('\n'
                     'line 3\n'
                     'line 4\n'
                     'line 5\n'
                     'line 6\n'
                     'line 7\n')
            try:
                parse.make_stanzas(text)
                assert False, 'No line between stanzas'
            except SyntaxError:
                pass

        def test_is_valid_haiku_positive(self):
            text = ('this is a test line\n'
                    'this is another test line\n'
                    'the final test line')
            assert parse.is_valid_haiku(text), 'Stanza follows 5-7-5 pattern'

        def test_is_valid_haiku_negative(self):
            text = ('this is not a haiku\n'
                    'this is another test line\n'
                    'the final test line')
            assert parse.is_valid_haiku(text) == False, 'Stanza is 6-7-5'

        def test_make_tokens_basic(self):
            raw = 'heaven more reduce petal up descend hear speak some'
            out = parse.make_tokens(raw)
            assert out == [parse.ParserToken(interpret.TokenType.HEAVEN),
                           parse.ParserToken(interpret.TokenType.PROMOTE),
                           parse.ParserToken(interpret.TokenType.DEMOTE),
                           parse.ParserToken(interpret.TokenType.BLOSSOM),
                           parse.ParserToken(interpret.TokenType.RISE),
                           parse.ParserToken(interpret.TokenType.FALL),
                           parse.ParserToken(interpret.TokenType.LISTEN),
                           parse.ParserToken(interpret.TokenType.SPEAK),
                           parse.ParserToken(interpret.TokenType.RAND)], out

        def test_make_tokens_numbers(self):
            raw = 'zero a dozen century fifteenth three-\nhundred-fifty-two'
            out = parse.make_tokens(raw)
            assert out == [parse.ParserToken(interpret.TokenType.INT, 0),
                           parse.ParserToken(interpret.TokenType.INT, 1),
                           parse.ParserToken(interpret.TokenType.INT, 12),
                           parse.ParserToken(interpret.TokenType.INT, 100),
                           parse.ParserToken(interpret.TokenType.INT, 15),
                           parse.ParserToken(interpret.TokenType.INT, 352)], out

        def test_make_tokens_var(self):
            raw = 'tree flame rock metal bogus'
            out = parse.make_tokens(raw)
            assert out == [parse.ParserToken(interpret.TokenType.VAR,
                                             interpret.VariableToken('tree', interpret.ElementType.WOOD)),
                           parse.ParserToken(interpret.TokenType.VAR,
                                             interpret.VariableToken('flame', interpret.ElementType.FIRE)),
                           parse.ParserToken(interpret.TokenType.VAR,
                                             interpret.VariableToken('rock', interpret.ElementType.EARTH)),
                           parse.ParserToken(interpret.TokenType.VAR,
                                             interpret.VariableToken('metal', interpret.ElementType.METAL)),
                           parse.ParserToken(interpret.TokenType.VAR,
                                             interpret.VariableToken('bogus', interpret.ElementType.EARTH))
                           ], out

        def test_make_tokens_comments(self):
            raw = 'heaven, some, not'
            out = parse.make_tokens(raw)
            assert out == [parse.ParserToken(interpret.TokenType.HEAVEN),
                           parse.ParserToken(parse.ParserTokenType.COMMA),
                           parse.ParserToken(interpret.TokenType.RAND),
                           parse.ParserToken(parse.ParserTokenType.COMMA),
                           parse.ParserToken(interpret.TokenType.NEGATIVE)], out

        def test_is_balanced_negative(self):
            program = [parse.ParserToken(interpret.TokenType.INT, 1),
                       parse.ParserToken(parse.ParserTokenType.COMMA),
                       parse.ParserToken(interpret.TokenType.INT, 2),
                       parse.ParserToken(parse.ParserTokenType.COMMA),
                       parse.ParserToken(interpret.TokenType.INT, 2),
                       parse.ParserToken(interpret.TokenType.RAND)]
            assert parse.is_balanced(program) == False, 'Yin/yang values are 2/1, not 1/1'

        def test_is_balanced_positive(self):
            program = [parse.ParserToken(parse.ParserTokenType.COMMA),
                       parse.ParserToken(interpret.TokenType.RAND),
                       parse.ParserToken(parse.ParserTokenType.COMMA)]
            assert parse.is_balanced(program), '0 values is balanced'
            program.append(parse.ParserToken(interpret.TokenType.INT, 1))
            program.append(parse.ParserToken(interpret.TokenType.INT, 2))
            assert parse.is_balanced(program), '1 of each is balanced'

        def test_remove_comments(self):
            program = []
            assert parse.remove_comments(program) == [], 'Empty is unchanged'
            program = [parse.ParserToken(parse.ParserTokenType.COMMA),
                       parse.ParserToken(interpret.TokenType.PUNC),
                       parse.ParserToken(parse.ParserTokenType.COMMA)]
            assert parse.remove_comments(program) == [], 'Only comments is empty'
            program.append(parse.ParserToken(interpret.TokenType.PUNC))
            result = parse.remove_comments(program)
            assert result == [interpret.Token(interpret.TokenType.PUNC)]


class TestLineCoverage:
    class TestParse:
        pass

    class TestInternals:
        pass