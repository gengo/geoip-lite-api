FROM python:alpine3.15 AS base
MAINTAINER Gengo Dev Team
RUN apk add build-base linux-headers pcre-dev
RUN pip install uwsgi==2.0.18 && pip install awscli

FROM base as app
WORKDIR /srv
COPY . /srv

RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/sh", "run.sh"]
