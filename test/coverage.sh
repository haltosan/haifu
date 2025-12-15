#!/bin/bash

cd ..
coverage run --data-file=test/coverage/pytest.dat -m pytest

# haifu.py
coverage run --data-file=test/coverage/no_file.dat haifu.py bogus
coverage run --data-file=test/coverage/syntax_error.dat haifu.py test/inputs/syntax_error.haifu
coverage run --data-file=test/coverage/success.dat haifu.py examples/123.haifu 1
coverage run --data-file=test/coverage/success2.dat haifu.py examples/123.haifu 0
coverage run --data-file=test/coverage/args.dat haifu.py
coverage run --data-file=test/coverage/args2.dat haifu.py examples/123.haifu bogus


coverage combine test/coverage/*.dat
coverage report
coverage html