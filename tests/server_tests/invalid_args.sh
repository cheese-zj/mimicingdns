#!/bin/bash


coverage run --append server.py tests/server_tests/sample_no_this.conf &
sleep 2

coverage run --append server.py &
sleep 2

coverage run --append server.py tests/server_tests/sample_bad.conf &
sleep 2

coverage run --append server.py tests/server_tests/sample_bad_port.conf &
sleep 2

coverage run --append server.py tests/server_tests/sample.conf &
sleep 2
coverage run --append server.py tests/server_tests/sample.conf &

printf '!EXIT\n' | ncat localhost 1024
sleep 0.2


#coverage report -m