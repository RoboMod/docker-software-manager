#!/bin/bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

URL="https://github.com/docker/compose"

LATEST_VERSION_URL=`curl -s -L -I $URL/releases/latest | grep Location | cut -d' ' -f2`
LATEST_VERSION=`echo $LATEST_VERSION_URL | rev | cut -d'/' -f1 | rev | sed 's/^[ \t\r]*//g' | sed 's/[ \t\r]*$//g'`

if [ ! -f "$BASEDIR/docker-compose-Linux-x86_64-$LATEST_VERSION" ]
then
    cd $BASEDIR
    wget $URL/releases/download/$LATEST_VERSION/docker-compose-Linux-x86_64 -O docker-compose-Linux-x86_64-$LATEST_VERSION
    cp docker-compose-Linux-x86_64-$LATEST_VERSION docker-compose
    chmod +x docker-compose
else
    echo "Up to date"
fi