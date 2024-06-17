#!/bin/bash
NAME="prod_memcached"
SOCKETFILE="/home/prod_user/prod_project/prod_memcached.sock"
USER=prod_user
MEMORYUSAGE=128

#-d don't need this as will be used with supervisor

exec memcached -m $MEMORYUSAGE -u $USER memory -s $SOCKETFILE
