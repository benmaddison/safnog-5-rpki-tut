FROM ubuntu:latest

WORKDIR /root

RUN apt update -q && \
    apt install -yq iproute2 iputils-ping iputils-tracepath \
                    python3 python3-pip ssh vim

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
RUN chmod +x deploy.py

ENTRYPOINT ./deploy.py --wait --delay 10
