from faker.providers.geo import Provider as GeoProvider


class Provider(GeoProvider):

    def local_latitude(self):
        return self.coordinate(center=46.7716, radius=0.5)

    def local_longitude(self):
        return self.coordinate(center=7.0382, radius=0.25)
