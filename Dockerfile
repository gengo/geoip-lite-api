FROM python:3.8.5-slim-buster
MAINTAINER Gengo Dev Team

ARG uid=1000

RUN apt-get -y update && apt-get -y install build-essential

RUN pip install --upgrade pip

RUN adduser -u ${uid} --disabled-password --disabled-login --gecos python python
RUN chown python /srv
USER python

WORKDIR /srv
COPY . /srv

ENV PATH "/home/python/.local/bin:$PATH"
RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/sh", "run.sh"]
