import pathlib

import pytest

import haifu_common
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
            assert out == [haifu_common.Token(haifu_common.TokenType.HEAVEN)], out

        def test_parse_print_123(self):
            raw = ('heaven count rise count\n'
                   'rise count three two one, four test\n'
                   'longer longer test')
            out = self.raw_to_out(raw)
            assert out == [haifu_common.Token(haifu_common.TokenType.INT, 1),
                           haifu_common.Token(haifu_common.TokenType.INT, 2),
                           haifu_common.Token(haifu_common.TokenType.INT, 3),
                           haifu_common.Token(haifu_common.TokenType.COUNT),
                           haifu_common.Token(haifu_common.TokenType.RISE),
                           haifu_common.Token(haifu_common.TokenType.COUNT),
                           haifu_common.Token(haifu_common.TokenType.RISE),
                           haifu_common.Token(haifu_common.TokenType.COUNT),
                           haifu_common.Token(haifu_common.TokenType.HEAVEN)], out

        def test_parse_print_var_elements(self):
            raw = ('tree flame metal ice\n'
                   'soil spirit, and pumpkin spice\n'
                   'longer longer test')
            out = self.raw_to_out(raw)
            assert out == [
                haifu_common.Token(haifu_common.TokenType.VAR,
                                 haifu_common.VariableToken('spirit', haifu_common.ElementType.EARTH)),
                haifu_common.Token(haifu_common.TokenType.VAR,
                                 haifu_common.VariableToken('soil', haifu_common.ElementType.EARTH)),
                haifu_common.Token(haifu_common.TokenType.VAR,
                                 haifu_common.VariableToken('ice', haifu_common.ElementType.WATER)),
                haifu_common.Token(haifu_common.TokenType.VAR,
                                 haifu_common.VariableToken('metal', haifu_common.ElementType.METAL)),
                haifu_common.Token(haifu_common.TokenType.VAR,
                                 haifu_common.VariableToken('flame', haifu_common.ElementType.FIRE)),
                haifu_common.Token(haifu_common.TokenType.VAR,
                                 haifu_common.VariableToken('tree', haifu_common.ElementType.WOOD))
            ], out

        def test_parse_vulgar(self):
            raw = ('fuck longer longer\n'
                   'longer longer longer test\n'
                   'longer longer test')
            try:
                self.raw_to_out(raw)
            except SyntaxError as e:
                assert 'Program contains vulgar word' in e.msg
                return
            assert False, 'raw contains vulgar words'

        def test_parse_invalid_stanzas(self):
            raw = ('longer longer test\n'
                   'longer longer longer test')
            try:
                self.raw_to_out(raw)
            except SyntaxError as e:
                assert 'Improper number of lines' in e.msg
                return
            assert False, 'raw does not have valid line count'

        def test_parse_invalid_haiku(self):
            raw = ('longer longer test\n'
                   'wrong\n'
                   'longer longer test')
            try:
                self.raw_to_out(raw)
            except SyntaxError as e:
                assert 'Not valid haiku' in e.msg
                return
            assert False, 'raw does not follow haiku structure'

        def test_parse_yin_yang_imbalance(self):
            raw = ('one two three four five\n'
                   'heaven heaven heaven rise\n'
                   'heaven heaven rise')
            try:
                self.raw_to_out(raw)
            except SyntaxError as e:
                assert e.msg == 'Yin and yang are not balanced'
                return
            assert False, 'raw has imbalance of yin and yang'


    class TestInternals:
        def test_read_file_negative(self):
            file_name = 'nonexist.txt'
            try:
                pathlib.Path(file_name).unlink()
            except FileNotFoundError:
                pass
            try:
                parse.read_file(file_name)
            except FileNotFoundError:
                return
            assert False, 'File does not exist, should error'

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

        def test_find_vulgar_positive(self):
            raw = 'mother fucker'
            assert parse.find_vulgar(raw) is not None, 'raw contains vulgar'

            raw = 'ass goblin'
            assert parse.find_vulgar(raw) is not None, 'raw contains vulgar'

        def test_find_vulgar_negative(self):
            raw = 'brass cumin'
            out = parse.find_vulgar(raw)
            assert out is None, 'raw is not vulgar: ' + out

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
            assert out == [parse.ParserToken(haifu_common.TokenType.HEAVEN),
                           parse.ParserToken(haifu_common.TokenType.PROMOTE),
                           parse.ParserToken(haifu_common.TokenType.DEMOTE),
                           parse.ParserToken(haifu_common.TokenType.BLOSSOM),
                           parse.ParserToken(haifu_common.TokenType.RISE),
                           parse.ParserToken(haifu_common.TokenType.FALL),
                           parse.ParserToken(haifu_common.TokenType.LISTEN),
                           parse.ParserToken(haifu_common.TokenType.SPEAK),
                           parse.ParserToken(haifu_common.TokenType.RAND)], out

        def test_make_tokens_numbers(self):
            raw = 'zero a dozen century fifteenth three-\nhundred-fifty-two'
            out = parse.make_tokens(raw)
            assert out == [parse.ParserToken(haifu_common.TokenType.INT, 0),
                           parse.ParserToken(haifu_common.TokenType.INT, 1),
                           parse.ParserToken(haifu_common.TokenType.INT, 12),
                           parse.ParserToken(haifu_common.TokenType.INT, 100),
                           parse.ParserToken(haifu_common.TokenType.INT, 15),
                           parse.ParserToken(haifu_common.TokenType.INT, 352)], out

        def test_make_tokens_var(self):
            raw = 'tree flame rock metal bogus'
            out = parse.make_tokens(raw)
            assert out == [parse.ParserToken(haifu_common.TokenType.VAR,
                                             haifu_common.VariableToken('tree', haifu_common.ElementType.WOOD)),
                           parse.ParserToken(haifu_common.TokenType.VAR,
                                             haifu_common.VariableToken('flame', haifu_common.ElementType.FIRE)),
                           parse.ParserToken(haifu_common.TokenType.VAR,
                                             haifu_common.VariableToken('rock', haifu_common.ElementType.EARTH)),
                           parse.ParserToken(haifu_common.TokenType.VAR,
                                             haifu_common.VariableToken('metal', haifu_common.ElementType.METAL)),
                           parse.ParserToken(haifu_common.TokenType.VAR,
                                             haifu_common.VariableToken('bogus', haifu_common.ElementType.EARTH))
                           ], out

        def test_make_tokens_comments(self):
            raw = 'heaven, some, not'
            out = parse.make_tokens(raw)
            assert out == [parse.ParserToken(haifu_common.TokenType.HEAVEN),
                           parse.ParserToken(haifu_common.TokenType.COMMA),
                           parse.ParserToken(haifu_common.TokenType.RAND),
                           parse.ParserToken(haifu_common.TokenType.COMMA),
                           parse.ParserToken(haifu_common.TokenType.NEGATIVE)], out

        def test_is_balanced_negative(self):
            program = [parse.ParserToken(haifu_common.TokenType.INT, 1),
                       parse.ParserToken(haifu_common.TokenType.COMMA),
                       parse.ParserToken(haifu_common.TokenType.INT, 2),
                       parse.ParserToken(haifu_common.TokenType.COMMA),
                       parse.ParserToken(haifu_common.TokenType.INT, 2),
                       parse.ParserToken(haifu_common.TokenType.RAND)]
            assert parse.is_balanced(program) == False, 'Yin/yang values are 2/1, not 1/1'

        def test_is_balanced_positive(self):
            program = [parse.ParserToken(haifu_common.TokenType.COMMA),
                       parse.ParserToken(haifu_common.TokenType.RAND),
                       parse.ParserToken(haifu_common.TokenType.COMMA)]
            assert parse.is_balanced(program), '0 values is balanced'
            program.append(parse.ParserToken(haifu_common.TokenType.INT, 1))
            program.append(parse.ParserToken(haifu_common.TokenType.INT, 2))
            assert parse.is_balanced(program), '1 of each is balanced'

        def test_remove_comments(self):
            program = []
            assert parse.remove_comments(program) == [], 'Empty is unchanged'
            program = [parse.ParserToken(haifu_common.TokenType.COMMA),
                       parse.ParserToken(haifu_common.TokenType.PUNC),
                       parse.ParserToken(haifu_common.TokenType.COMMA)]
            assert parse.remove_comments(program) == [], 'Only comments is empty'
            program.append(parse.ParserToken(haifu_common.TokenType.PUNC))
            result = parse.remove_comments(program)
            assert result == [haifu_common.Token(haifu_common.TokenType.PUNC)]


class TestLineCoverage:
    class TestParse:
        pass

    class TestInternals:
        pass