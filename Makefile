.PHONY: console build

console: build
	docker run -it -v="$(PWD):/braintree-python" --net="host" braintree-python /bin/bash -l -c "pip3 install -r dev_requirements.txt;pip3 install pylint;bash"

build:
	docker build -t braintree-python .
