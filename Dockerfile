FROM alpine:latest

RUN apk add ca-certificates python3 supervisor

WORKDIR /app

COPY docker/dn42.crt /usr/local/share/ca-certificates/dn42.crt
RUN update-ca-certificates

COPY . .

RUN mkdir /app/data && ln -s ../docker/servers.example.json /app/data/servers.json

ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/app/docker/supervisord.conf"]
