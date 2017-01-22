FROM ubuntu:16.04
MAINTAINER Claudio Sparpaglione <csparpa@gmail.com>

# Install linux packages
RUN apt-get update && \
    apt-get -y install software-properties-common apt-utils wget

# Add fkrull/deadsnakes PPA and install python versions
RUN add-apt-repository ppa:fkrull/deadsnakes && \
    apt-get update
RUN apt-get install -y python2.7 python3.2 python3.3 python3.4 python3.5 python3.6 \
    python-pip ipython ipython3 python3-setuptools zlib1g-dev

# Install setuptools and setuptools3
RUN wget https://bootstrap.pypa.io/ez_setup.py -O - | python && \
    wget https://bootstrap.pypa.io/ez_setup.py -O - | python3

# Mount latest source code
ADD . /pyowm
WORKDIR /pyowm

# Update pip and install dev requirements
RUN pip install --upgrade setuptools pip && \
    pip install -r /pyowm/dev-requirements.txt

CMD tail -f /dev/null
