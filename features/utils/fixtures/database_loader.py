from django.conf import settings
from features.utils.auth.account_handling import create_database_user
from features.utils.fixtures import json

import os


def load_user_data_in_database(user_data, persona):
    result = []
    if isinstance(user_data, list):
        for user in user_data:
            stored_user = create_database_user(user)
            assert stored_user.pk == user['id'], '[%s] - %d should equal %d' % (
                persona, stored_user.pk, user['id'])
            result.append(user)
    else:
        stored_user = create_database_user(user_data)
        assert stored_user.pk == user_data['id'], '[%s] - %d should equal %d' % (
            persona, stored_user.pk, user_data['id'])
        result.append(user_data)
    return result


def load_persona_in_database(path_to_users, persona):
    user_data = json.load(os.path.join(path_to_users, persona + '.json'))
    return load_user_data_in_database(user_data, persona)


def load_users_in_database(variant):

    path_to_users = os.path.join(settings.FIXTURE_DIRS[0], variant, 'Users')

    consumers = load_persona_in_database(path_to_users, 'Consommateurs')
    producers = load_persona_in_database(path_to_users, 'Producteurs')
    managers = load_persona_in_database(path_to_users, 'Responsables')
    reges = load_persona_in_database(path_to_users, 'Rex')
    softozors = load_persona_in_database(path_to_users, 'Softozor')

    return consumers, producers, managers, reges, softozors
