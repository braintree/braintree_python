#!/usr/bin/env sh
python3 setup.py sdist
pip wheel . -w dist
twine upload dist/braintree-*
