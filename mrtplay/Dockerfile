# BUILD stage
FROM python:3-buster as build

ARG PEER_AS
ARG IPV4_NEXTHOP
ARG IPV6_NEXTHOP

WORKDIR /root

RUN pip install mrtparse

COPY mrt2exabgp.py .
RUN chmod +x mrt2exabgp.py

COPY latest-bview.gz .
RUN ./mrt2exabgp.py -p ${PEER_AS} -4 ${IPV4_NEXTHOP} -s -G -P latest-bview.gz > announce4.py
RUN ./mrt2exabgp.py -p ${PEER_AS} -6 ${IPV6_NEXTHOP} -s -G -P latest-bview.gz > announce6.py

# FINAL stage
FROM python:3-buster

RUN pip install exabgp

WORKDIR /usr/local/run/exabgp
RUN mkfifo exabgp.in exabgp.out
RUN chmod 600 exabgp.*

WORKDIR /usr/local/etc/exabgp
COPY exabgp.* ./
COPY --from=build /root/announce*.py ./
RUN chmod +x announce*.py

ENTRYPOINT exabgp /usr/local/etc/exabgp/exabgp.conf
