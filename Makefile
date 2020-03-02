.PHONY: console build

console: build
	docker run -it -v="$(PWD):/braintree-python" --net="host" braintree-python /bin/bash -l -c "pip install -r dev_requirements.txt;bash"

build:
	docker build -t braintree-python .
