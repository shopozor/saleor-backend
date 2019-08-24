export DJANGO_SETTINGS_MODULE=shopozor.settings

# Generate django fixtures
python manage.py generate_django_fixtures --settings features.settings

# Generate the Users with passwords
./scripts/resetDB.sh && python manage.py setup_e2e_data --fixture-variant small --settings features.settings
./scripts/resetDB.sh && python manage.py setup_e2e_data --fixture-variant medium --settings features.settings
./scripts/resetDB.sh && python manage.py setup_e2e_data --fixture-variant large --settings features.settings

# Generate the graphql responses corresponding to the django fixtures
python manage.py generate_graphql_responses --settings features.settings
