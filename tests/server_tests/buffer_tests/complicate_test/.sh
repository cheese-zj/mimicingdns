#!/bin/bash
config_input="tests/server_tests/sample.conf"

coverage run --append server.py $config_input > tests/tmp.actual.out &
sleep 2

msg=$(cat tests/server_tests/buffer_tests/complicate_test/.in)
msg2=$(cat tests/server_tests/buffer_tests/complicate_test/newline.in)

printf "$msg" | ncat localhost 1024
sleep 0.2

printf "$msg2" | ncat localhost 1024
sleep 0.2

# printf '!EXIT\n' | ncat localhost 1024
# sleep 0.2

echo "From msg test: $msg and $msg2"

echo "DIFF:"
diff tests/tmp.actual.out tests/server_tests/buffer_tests/complicate_test/.out
echo