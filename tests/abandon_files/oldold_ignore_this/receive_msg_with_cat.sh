#!/bin/bash

# start a hard-coded server in background by coverage



echo sending to server!!!!!

for file in ./tests/server_tests/ins_outs/*.in; do
    coverage run --append server.py tests/server_tests/sample.conf &
    sleep 2
    base_filename=$(basename "$file" .in)
    cat "$file" | ncat localhost 1024 > "./tests/server_tests/ins_outs/$base_filename.actual" &
    pid=$!
    sleep 0.2
    kill $pid  # Terminate the ncat process
    printf '!EXIT\n' | ncat localhost 1024 &
    sleep 0.2
done

echo sends EXIT?

# terminate the server by sending EXIT command



