FROM python:3.8.5-slim-buster AS base
MAINTAINER Gengo Dev Team

ARG uid=1000

RUN apt-get -y update
RUN apt-get -y install build-essential
RUN pip install --upgrade pip

RUN adduser -u ${uid} --disabled-password --disabled-login --gecos python python
USER python

RUN pip install uwsgi==2.0.21 awscli

FROM base as app
WORKDIR /srv
COPY . /srv

RUN pip install --no-warn-script-location -r requirements.txt
ENTRYPOINT ["/bin/sh", "run.sh"]
