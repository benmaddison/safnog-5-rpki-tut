FROM ubuntu:latest

WORKDIR /root

RUN apt update -q && \
    apt install -yq python python-pip

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /usr/local/run/exabgp
RUN mkfifo exabgp.in exabgp.out
RUN chmod 600 exabgp.*
# RUN chown nobody /usr/local/run/exabgp/exabgp.*

# RUN chown nobody announce.py
WORKDIR /usr/local/etc/exabgp
COPY exabgp.* ./
COPY announce.py .
RUN chmod +x announce.py

# RUN chmod +x mrt2exabgp.py
# RUN ./mrt2exabgp.py
# ENTRYPOINT ./mrt2exabgp.py -G 1000 latest-bview.gz

ENTRYPOINT exabgp /usr/local/etc/exabgp/exabgp.conf
# ENTRYPOINT sh -c "while true; do sleep 1; done"
