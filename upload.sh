#!/bin/sh

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VERSION=`python $BASEDIR/setup.py --version`

twine upload $BASEDIR/dist/docker_software_manager-$VERSION* $BASEDIR/dist/docker-software-manager-$VERSION.tar.gz