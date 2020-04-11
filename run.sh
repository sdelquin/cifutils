#!/bin/bash

source ~/.virtualenvs/cifutils/bin/activate
cd "$(dirname "$0")"
exec gunicorn -c gunicorn.conf.py cifutils.wsgi:application
