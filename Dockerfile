FROM python:3.8-alpine
MAINTAINER Pythontr.Com Huseyin OZDEMIR

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# WARNING: Ignoring APKINDEX.5a59b88b.tar.gz: No such file or directory
# WARNING: Ignoring APKINDEX.7c1f02d6.tar.gz: No such file or directory
# Added two lines after that for warnings
RUN rm -rf /var/cache/apk/* && \
    rm -rf /tmp/*
RUN apk update
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN adduser -D user
USER user
