#!/bin/bash

LINK="/usr/local/bin/docker-compose"

if [ -h "$LINK" ]
then
    rm $LINK
fi