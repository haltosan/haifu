import pathlib

import parse
import interpret
from parse import make_stanzas


class TestContract:
    class TestParse:
        pass

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
            assert len(result) == 1, 'Only 1 non-comment'
            assert type(result[0]) is parse.ParserToken
            assert result[0].t == interpret.TokenType.PUNC


class TestLineCoverage:
    class TestParse:
        pass

    class TestInternals:
        pass