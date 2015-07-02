#!/bin/bash

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# install docker-gen binary link
LINK="/usr/local/bin/docker-gen"
if [ ! -h "$LINK" ]
then
    ln -s $BASEDIR/docker-gen $LINK
fi

# install docker-gen nginx sites link
LINK="/etc/nginx/sites-enabled/docker-sites"
TARGET="/etc/nginx/sites-available/docker-sites"
if [ ! -h "$LINK" ]
then
    ln -s $TARGET $LINK
fi

## install docker-gen nginx systemd service
##LINK="/etc/systemd/system/docker-gen-nginx.service"
#LINK="/server/utils/docker-gen/docker-gen-nginx.service"
##if [ ! -h "$LINK" ]
##then
#    #ln -s $BASEDIR/docker-gen-nginx.service $LINK
#    systemctl enable $LINK
##fi