from dateutil import tz
from dateutil.relativedelta import relativedelta
from faker.providers.date_time import Provider as DateTimeProvider


class Provider(DateTimeProvider):

    def conservation_until(self, start_date):
        end_date = start_date + relativedelta(years=1)
        return self.date_time_between_dates(datetime_start=start_date, datetime_end=end_date, tzinfo=tz.tzutc()).isoformat()

    def publication_date(self):
        return self.date_time_between_dates(tzinfo=tz.tzutc()).isoformat()