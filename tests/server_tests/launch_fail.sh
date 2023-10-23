#!/bin/bash

coverage run --append server.py tests/server_tests/sample_bad.conf &
sleep 2


echo fake recursor sends bad EXIT

# terminate the server by sending EXIT command
printf '!EXIT\n' | ncat localhost 1088




