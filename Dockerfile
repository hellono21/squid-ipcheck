FROM jfloff/alpine-python:2.7

RUN apk upgrade --no-cache \
    && apk add --no-cache squid curl

# forward request and error logs to docker log collector
#RUN ln -sf /dev/stdout /var/log/squid/access.log

RUN pip install redis

COPY . .

EXPOSE 3128

ENTRYPOINT ["/entrypoint.sh"]
