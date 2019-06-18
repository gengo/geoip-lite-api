FROM python:3.7.3-alpine3.9 AS base
MAINTAINER Gengo Dev Team
RUN apk add build-base linux-headers pcre-dev
RUN pip install uwsgi && pip install awscli

FROM base as app
WORKDIR /srv
COPY . /srv

RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/sh", "run.sh"]
