#!/bin/bash
config_input=$(cat tests/server_tests/bad_launch_tests/conf_bad_port/.in)

echo "Launch Option $config_input"

coverage run --append server.py $config_input > tests/tmp.actual.out &
sleep 2

#coverage report -m
# compare the actual output and the expected output, but they are different!?
# THEY ARE NOT !!!!!!
echo "DIFF:"
diff tests/tmp.actual.out tests/server_tests/bad_launch_tests/conf_bad_port/.out
echo