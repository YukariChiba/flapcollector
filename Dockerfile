FROM node:alpine AS frontendbuilder

WORKDIR /app

COPY frontend .

RUN npm i && npm run build


FROM alpine:latest

RUN apk add ca-certificates python3 supervisor py3-flask

WORKDIR /app

COPY docker/dn42.crt /usr/local/share/ca-certificates/dn42.crt
RUN update-ca-certificates

COPY backend .
COPY --from=frontendbuilder /app/dist ./public

COPY docker/supervisord.conf .
ENTRYPOINT ["supervisord", "--nodaemon", "--configuration", "/app/supervisord.conf"]
