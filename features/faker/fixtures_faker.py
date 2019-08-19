from faker import Faker

import unidecode

fake = Faker('fr_CH')
fake.seed('features')


class UserFactory:
    def create_consumers(list_size=1):
        result = []
        for _ in range(0, list_size):
            result.append({
                'email': fake.email(),
                'isActive': True
            })
        return result

    def create_producers(list_size=1):
        result = []
        for _ in range(0, list_size):
            first_name = fake.first_name()
            last_name = fake.last_name()
            domain_name = fake.free_email_domain()
            result.append({
                # get rid of any potential French accent from the first and last name
                'email': unidecode.unidecode('%s.%s@%s' % (first_name, last_name, domain_name)),
                'isActive': True,
                'isStaff': True,
                'first_name': first_name,
                'last_name': last_name
            })
        return result

    def create_managers(list_size=1):
        result = []
        for _ in range(0, list_size):
            first_name = fake.first_name()
            last_name = fake.last_name()
            domain_name = fake.free_email_domain()
            result.append({
                # get rid of any potential French accent from the first and last name
                'email': unidecode.unidecode('%s.%s@%s' % (first_name, last_name, domain_name)),
                'isActive': True,
                'isStaff': True,
                'first_name': first_name,
                'last_name': last_name,
                'permissions': [{
                    'code': 'MANAGE_PRODUCERS'
                }]
            })
        return result
