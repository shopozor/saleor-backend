from django.conf import settings
from features.utils.auth.account_handling import create_database_user
from features.utils.fixtures import json

import os


def load_users_in_database(variant):
    users = []
    for persona in 'Consommateurs', 'Producteurs', 'Responsables', 'Rex', 'Softozor':
        user_data = json.load(os.path.join(
            settings.FIXTURE_DIRS[0], variant, 'Users', persona + '.json'))
        if isinstance(user_data, list):
            for user in user_data:
                stored_user = create_database_user(user)
                assert stored_user.pk == user['id'], '[%s] - %d should equal %d' % (
                    persona, stored_user.pk, user['id'])
                users.append(user)
        else:
            stored_user = create_database_user(user_data)
            assert stored_user.pk == user_data['id'], '[%s] - %d should equal %d' % (
                persona, stored_user.pk, user_data['id'])
            users.append(user_data)
    return users
