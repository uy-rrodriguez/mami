#!/bin/bash

PREFIX_ADDR_ES="inet"
PREFIX_ADDR_FR="inet adr"

uname=$(uname -a)
name=$(echo $uname | cut -f2 -d" ")

ifconfig=$(ifconfig | grep -F "$PREFIX_ADDR_FR:" | grep -Fv "$PREFIX_ADDR_FR:127.0.0.1")
ip=$(echo $ifconfig | sed "s/.*$PREFIX_ADDR_FR:\([0-9]\{1,3\}\(\.[0-9]\{1,3\}\)\{3\}\).*/\1/")

if [ -z $ip ]
then
    ifconfig=$(ifconfig | grep -F "$PREFIX_ADDR_ES:" | grep -Fv "$PREFIX_ADDR_ES:127.0.0.1")
    ip=$(echo $ifconfig | sed "s/.*$PREFIX_ADDR_ES:\([0-9]\{1,3\}\(\.[0-9]\{1,3\}\)\{3\}\).*/\1/")
fi

uptime=$(top -b -n 1 | grep " up " | sed "s/.*up\( \)\{1,2\}\([0-9]\{1,2\}:[0-9][0-9]\).*/\2/")

echo "$name|$ip|$uptime|"
