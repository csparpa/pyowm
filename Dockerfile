FROM ubuntu:15.10
MAINTAINER Claudio Sparpaglione <csparpa@gmail.com>

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get -y install software-properties-common wget && \
RUN echo -ne '\n' |  apt-add-repository ppa:fkrull/deadsnakes
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install python2.7 python3.2 python3.3 python3.5 python-pip -y
RUN wget https://bootstrap.pypa.io/ez_setup.py -O - | python && \
    wget https://bootstrap.pypa.io/ez_setup.py -O - | python3

ADD . /pyowm
WORKDIR /pyowm

RUN pip install -r /pyowm/dev-requirements.txt

CMD tail -f /dev/null
