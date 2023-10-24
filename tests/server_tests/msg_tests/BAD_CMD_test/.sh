#!/bin/bash
config_input="tests/server_tests/sample.conf"

coverage run --append server.py $config_input > tests/tmp.actual.out &
sleep 2

msg=$(cat tests/server_tests/msg_tests/BAD_CMD_test/.in)

printf "$msg" | ncat localhost 1024
sleep 0.2

printf '!EXIT\n' | ncat localhost 1024
sleep 0.2

echo "From msg test: $msg"

echo "DIFF:"
diff tests/tmp.actual.out tests/server_tests/msg_tests/BAD_CMD_test/.out
echo