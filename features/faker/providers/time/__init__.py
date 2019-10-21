from dateutil.relativedelta import relativedelta
from faker.providers.date_time import Provider as DateTimeProvider


class Provider(DateTimeProvider):

    def conservation_days(self):
        return self.random_int(1, 60)

    def publication_date(self):
        return self.date_between_dates().isoformat()