#!/bin/bash
# inthelab: set up the hello server on first boot.
# User data runs once, as root, the first time the server starts.
mkdir -p /opt/hello
curl -fsSL https://inthelab.ie/files/hello-server.py -o /opt/hello/hello-server.py
curl -fsSL https://inthelab.ie/files/hello.service -o /etc/systemd/system/hello.service
systemctl daemon-reload
systemctl enable --now hello