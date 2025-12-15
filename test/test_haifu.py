"""
Full integration tests of haifu.py
"""
import haifu


class TestContract:
    def test_haifu_123(self, capsys):
        haifu.run('examples/123.haifu', 1)
        out, err = capsys.readouterr()
        assert out == '123', err

    def test_haifu_hello_world(self, capsys):
        haifu.run('examples/hello_world.haifu', 1)
        out, err = capsys.readouterr()
        assert out == 'hello world\n', err

    def test_haifu_math(self, capsys):
        haifu.run('examples/math.haifu', 1)
        out, err = capsys.readouterr()
        assert out == '311.333333333333333320', err

    def test_haifu_print_function(self, capsys):
        haifu.run('examples/print-function.haifu', 1)
        out, err = capsys.readouterr()
        assert out == '111'