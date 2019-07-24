import factory
from saleor.core.utils.random_data import SaleorProvider

factory.Faker.add_provider(SaleorProvider)
