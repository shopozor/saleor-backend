#! /bin/bash

VARIANT=${1:-medium}

python3 manage.py migrate
python3 manage.py generate_django_fixtures --settings features.settings --fixture-variant $VARIANT
python3 manage.py setup_e2e_data --settings features.settings --fixture-variant $VARIANT