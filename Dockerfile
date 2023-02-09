FROM python:3.8.5-slim-buster
MAINTAINER Gengo Dev Team

RUN apt-get -y update && apt-get -y install build-essential

WORKDIR /srv
COPY . /srv

RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/sh", "run.sh"]
