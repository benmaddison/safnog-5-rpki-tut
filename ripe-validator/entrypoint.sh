#!/usr/bin/env bash

if [ ! -z "$VERSION" ]; then
  /opt/rpki-validator-${VERSION}/rpki-validator-3.sh &
  /opt/rpki-rtr-server-${VERSION}/rpki-rtr-server.sh &
fi

while true; do
  sleep 1
done
