#!/bin/bash

if [[ "$1" == "http" ]]; then
  python_tests="test:http"
fi

env PATH=/usr/local/python/2.7.1/bin:$PATH rake $python_tests --trace
