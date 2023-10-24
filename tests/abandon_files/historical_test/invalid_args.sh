#!/bin/bash


coverage run --append server.py tests/server_tests/sample_no_this.conf > ~/nxdomain/tests/tmp.actual.out &
sleep 2

coverage run --append server.py > ~/nxdomain/tests/tmp.actual.out &
sleep 2

coverage run --append server.py tests/server_tests/sample_bad.conf > ~/nxdomain/tests/tmp.actual.out &
sleep 2

coverage run --append server.py tests/server_tests/sample_bad_port.conf > ~/nxdomain/tests/tmp.actual.out &
sleep 2

coverage run --append server.py tests/server_tests/sample.conf > ~/nxdomain/tests/tmp.actual.out &
sleep 2
coverage run --append server.py tests/server_tests/sample.conf > ~/nxdomain/tests/tmp.actual.out &

printf '!EXIT\n' | ncat localhost 1024
sleep 0.2


#coverage report -m