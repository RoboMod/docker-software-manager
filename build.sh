#!/bin/sh

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

python $BASEDIR/setup.py sdist
python $BASEDIR/setup.py bdist_wheel