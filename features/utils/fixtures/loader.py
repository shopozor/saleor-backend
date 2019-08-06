import json
import os.path


def get_data_from_json_fixture(filename):
    with open(filename) as file:
        data = json.load(file)
    return data
