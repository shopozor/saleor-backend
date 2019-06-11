import json
import os.path

from django.conf import settings


def get_data_from_json_fixture(filename):
    fixture_filename = os.path.join(settings.FIXTURES_FOLDER, filename)
    with open(fixture_filename) as file:
        data = json.load(file)
    return data
