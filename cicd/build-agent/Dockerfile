FROM alpine:latest
RUN apk add --no-cache python3 py3-pip
RUN apk add --no-cache make
RUN apk add --no-cache aws-cli
RUN adduser -D python
USER python
WORKDIR /home/python
ENV PATH=$PATH:/home/python/.local/bin
