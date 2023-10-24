#!/bin/bash

# earse previous coverage
coverage erase

# write your own self-testing script at here!

# find . -type f -path "*server_tests*/*" -name '*.sh'
find . -type f -path "*server_tests*/*" -name '*.sh' -exec bash {} \;

coverage report -m

coverage html --directory tests/coverage_report