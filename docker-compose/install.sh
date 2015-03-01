#!/bin/bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# install docker-compose binary link
LINK="/usr/local/bin/docker-compose"
if [ ! -h "$LINK" ]
then
    ln -s $BASEDIR/docker-compose $LINK
fi