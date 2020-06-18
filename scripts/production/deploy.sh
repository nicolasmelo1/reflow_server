#!/bin/sh

#pypy3 manage.py collectstatic
pypy3 manage.py migrate
pypy3 manage.py loaddata fixtures/required_data.json
#pypy3 manage.py loaddata fixtures/initial_data.json
daphne -b 0.0.0.0 -p 8000 reflow_server.asgi:application
