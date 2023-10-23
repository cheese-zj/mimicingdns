#!/bin/bash

# start a hard-coded server in background by coverage
coverage run --append server.py tests/server_tests/sample.conf &
sleep 2


echo fake recursor sends ADD?

echo 'com' | ncat localhost 1024 &  # Send message to the server
pid=$!
sleep 0.2
kill $pid  # Terminate the ncat process

echo 'newdomain' | ncat localhost 1024 &  # Send message to the server
pid=$!
sleep 0.2
kill $pid  # Terminate the ncat process

echo '!BADCMD' | ncat localhost 1024 &  # Send message to the server
pid=$!
sleep 0.2
kill $pid  # Terminate the ncat process

echo '!ADD au 2000' | ncat localhost 1024 &  # Send message to the server
pid=$!
sleep 0.2
kill $pid  # Terminate the ncat process

echo '!ADD au 2001' | ncat localhost 1024 &  # Send message to the server
pid=$!
sleep 0.2
kill $pid  # Terminate the ncat process

echo '!DEL au' | ncat localhost 1024 &  # Send message to the server
pid=$!
sleep 0.2
kill $pid  # Terminate the ncat process

echo sends EXIT

# terminate the server by sending EXIT command
printf '!EXIT\n' | ncat localhost 1024

sleep 0.2


