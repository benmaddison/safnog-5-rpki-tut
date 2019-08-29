FROM ubuntu:latest

ARG VERSION=3.1-2019.08.19_09.00.01
ENV VERSION ${VERSION}

WORKDIR /opt

RUN apt update -q && \
    apt install -yq openjdk-8-jdk rsync wget

RUN wget -nv https://ftp.ripe.net/tools/rpki/validator3/prod/generic/rpki-rtr-server-${VERSION}-dist.tar.gz && \
    tar zxf rpki-rtr-server-${VERSION}-dist.tar.gz
RUN wget -nv https://ftp.ripe.net/tools/rpki/validator3/prod/generic/rpki-validator-${VERSION}-dist.tar.gz && \
    tar zxf rpki-validator-${VERSION}-dist.tar.gz

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ./entrypoint.sh
