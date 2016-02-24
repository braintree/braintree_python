#!/bin/bash

if [[ "$1" == "http" ]]; then
  python_tests="test:http"
fi

if [[ "$1" == "python3" ]]; then
  /usr/local/lib/python3.3/bin/nosetests-3.3
else
  env rake $python_tests --trace
fi
