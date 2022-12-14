#!/bin/bash

if [[ "$1" == "http" ]]; then
  python_tests="test:http"
fi

if [[ "$1" == "python3" ]]; then
  /usr/local/lib/python3.3/bin/python3 -m unittest discover
else
  env rake $python_tests --trace
fi
