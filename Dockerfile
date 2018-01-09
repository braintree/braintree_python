FROM debian:stretch

RUN apt-get update
RUN apt-get -y install python rake
RUN apt-get -y install python-pip
RUN pip install --upgrade pip
RUN pip install --upgrade distribute

WORKDIR /braintree-python
