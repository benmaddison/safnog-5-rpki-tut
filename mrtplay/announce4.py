#!/usr/bin/env python

import sys
import time

msgs = []

while msgs:
    msg = msgs.pop(0)
    if isinstance(msg, str):
        sys.stdout.write(msg + '\n')
        sys.stdout.flush()
    else:
        time.sleep(msg)

try:
    now = time.time()
    while True and time.time() < now + 5:
        line = sys.stdin.readline().strip()
        if not line or 'shutdown' in line:
            break
        time.sleep(1)
except IOError:
    pass
