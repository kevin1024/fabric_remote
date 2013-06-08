#!/bin/bash
eval `ssh-agent`
ssh-add /var/apps/.ssh/id_rsa
exec /var/apps/.virtualenvs/furoshiki/bin/gunicorn furoshiki:app -t 3000 -b unix:/var/apps/socks/furoshiki.sock
