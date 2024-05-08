from backend.discovery import multidiscovery
from backend.discovery import trip
import dateutil.parser

EXTERNAL_OFFSET = True
ENABLED = True
class Main(multidiscovery.Multidiscovery):
    def __init__(self):
        format = ('name', 'country', 'identifiers.flixbus')
        super().__init__(
            self.config.format_city_object(self.config.get_departure_city(), format),
            self.config.get_formatted_cities(format)
        )

    def get_date(self, offset=0):
        return super().get_date('%d.%m.%Y', offset)

    def search_location(self, p, offset):
        try:
            search = self.session.get('https://global.api.flixbus.com/search/service/v4/search',
            params={
                'from_city_id': self.departure[2],
                'to_city_id': p[2],
                'departure_date': self.get_date(offset),
                'products': '{"adult":1}',
                'currency': 'EUR',
                'locale': 'it',
                'search_by': 'cities',
                'include_after_midnight_rides': '1'
            }).json()
            for k in search.get('trips')[0]['results']:
                _trip = search.get('trips')[0]['results'][k]
                if (price := _trip['price']['total']) <= self.config.config.get('configuration').get('price_cap') and price > 0:
                    self.trips.append(
                        trip.Trip(
                            date=dateutil.parser.parse(_trip['departure']['date']),
                            departure=self.departure[0],
                            arrival=p[0],
                            carrier=self.base_name(__name__),
                            duration=(_trip['duration']['hours'] * 60) + _trip['duration']['minutes'],
                            price=price,
                            arrival_country=p[1]
                        )
                    )
        except:
            pass