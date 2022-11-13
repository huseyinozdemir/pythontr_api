FROM python:3.9-alpine3.13
LABEL maintainer="Pythontr.Com Huseyin OZDEMIR"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
#RUN mkdir /app
COPY . /app
WORKDIR /app
EXPOSE 8000
# WARNING: Ignoring APKINDEX.5a59b88b.tar.gz: No such file or directory
# WARNING: Ignoring APKINDEX.7c1f02d6.tar.gz: No such file or directory
# Added two lines after that for warnings
ARG DEV=false
RUN apk update
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /venv/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /var/cache/apk/* && \
    rm -rf /tmp/* && \
    adduser \
        --disabled-password \
        -D \
        user

RUN apk del .tmp-build-deps
ENV PATH="/venv/bin:$PATH"

USER user
