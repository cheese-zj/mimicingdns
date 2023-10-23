#!/bin/bash

# start a hard-coded server in background by coverage
coverage run --append server.py tests/server_tests/sample.conf &
sleep 2


echo fake recursor sends ADD?

echo 'com' | ncat localhost 1024 &  # Send message to the server
sleep 0.2

echo 'newdomain' | ncat localhost 1024 &  # Send message to the server
sleep 0.2

echo '!BADCMD' | ncat localhost 1024 &  # Send message to the server
sleep 0.2

echo '!ADD au 2000' | ncat localhost 1024 &  # Send message to the server
sleep 0.2

echo '!ADD au 2001' | ncat localhost 1024 &  # Send message to the server
sleep 0.2

echo '!DEL au' | ncat localhost 1024 &  # Send message to the server
sleep 0.2

printf 'co' | ncat localhost 1024 &  # Send message to the server
sleep 0.2

printf 'm\n' | ncat localhost 1024 &  # Send message to the server
sleep 0.2

echo sends EXIT

# terminate the server by sending EXIT command
printf '!EXIT\n' | ncat localhost 1024

sleep 0.2
