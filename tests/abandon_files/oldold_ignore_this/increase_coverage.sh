#!/bin/bash

coverage erase

coverage run --append test.py
coverage report -m # <- report coverage
coverage html --directory coverage_report # <- generate html report in this workspace

