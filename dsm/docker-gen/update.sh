#!/bin/bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

URL="https://github.com/jwilder/docker-gen"

LATEST_VERSION_URL=`curl -s -L -I $URL/releases/latest | grep Location | cut -d' ' -f2`
LATEST_VERSION=`echo $LATEST_VERSION_URL | rev | cut -d'/' -f1 | rev | sed 's/^[ \t\r]*//g' | sed 's/[ \t\r]*$//g'`

if [ ! -f "$BASEDIR/docker-gen-linux-amd64-$LATEST_VERSION.tar.gz" ]
then
    cd $BASEDIR
    wget $URL/releases/download/$LATEST_VERSION/docker-gen-linux-amd64-$LATEST_VERSION.tar.gz -O docker-gen-linux-amd64-$LATEST_VERSION.tar.gz
    tar xvzf docker-gen-linux-amd64-$LATEST_VERSION.tar.gz
else
    echo "Up to date"
fi