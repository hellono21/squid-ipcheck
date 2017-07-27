FROM jfloff/alpine-python:2.7

RUN apk upgrade --no-cache \
    && apk add --no-cache squid curl

RUN pip install redis

COPY . .

EXPOSE 3128

ENTRYPOINT ["/entrypoint.sh"]
