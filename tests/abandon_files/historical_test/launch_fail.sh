#!/bin/bash

coverage run --append server.py tests/server_tests/sample_bad_port.conf > ~/nxdomain/tests/tmp.actual.out &
sleep 2





