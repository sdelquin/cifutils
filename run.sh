#!/bin/bash

cd "$(dirname "$0")"
source .venv/bin/activate
exec gunicorn -b unix:/tmp/cifutils.sock cifutils.wsgi:application
