from faker.providers import BaseProvider


class Provider(BaseProvider):

    # TODO: make the length variable
    def variant_ids(self, elements, length):
        return self.random_elements(elements=elements, length=length, unique=True)
