FROM ubuntu:15.10
MAINTAINER Claudio Sparpaglione <csparpa@gmail.com>

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get -y install software-properties-common && \
    echo -ne '\n' |  apt-add-repository ppa:fkrull/deadsnakes && \
    apt-get upgrade -y && \
    apt-get install python 2.7 python3.2 python3.3 python-pip -y

RUN pip install -r dev-requirements.txt

ADD . /pyowm

WORKDIR /pyowm

CMD tail -f /dev/null
