#!/bin/bash

# remove binary link
LINK="/usr/local/bin/docker-gen"
if [ -h "$LINK" ]
then
    rm $LINK
fi

# remove nginx config link and config file
LINK="/etc/nginx/sites-enabled/docker-sites"
if [ -h "$LINK" ]
then
    rm $LINK
fi
FILE="/etc/nginx/sites-available/docker-sites"
if [ -f "$FILE" ]
then
    rm $FILE
fi

# remove systemd link
#LINK="/etc/systemd/system/docker-gen-nginx.service"
LINK="/server/utils/docker-gen/docker-gen-nginx.service"
#if [ -h "$LINK" ]
#then
    systemctl disable $LINK
    #rm $LINK
#fi