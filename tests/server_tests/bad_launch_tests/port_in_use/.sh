#!/bin/bash
config_input=$(cat tests/server_tests/bad_launch_tests/port_in_use/.in)

echo "Launch Option $config_input"

coverage run --append server.py $config_input &
sleep 2

coverage run --append server.py $config_input > tests/tmp.actual.out &
sleep 2

printf "!EXIT\n" | ncat localhost 1024

echo "DIFF:"
diff tests/tmp.actual.out tests/server_tests/bad_launch_tests/port_in_use/.out
echo