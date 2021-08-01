#!/bin/sh

python manage.py collectstatic
python manage.py migrate
python manage.py loaddata fixtures/required_data.json
python manage.py loaddata fixtures/address_data.json
#pypy3 manage.py loaddata fixtures/initial_data.json
daphne -b 0.0.0.0 -p 8000 reflow_server.asgi:application
