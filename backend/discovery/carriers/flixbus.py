from backend.discovery import multidiscovery
from backend.discovery.trip import Trip
import dateutil.parser

class Main(multidiscovery.Multidiscovery):
    EXTERNAL_OFFSET = True
    ENABLED = True

    def __init__(self):
        format = ('name', 'country', 'identifiers.flixbus')
        super().__init__(
            self.config.format_city_object(self.config.get_departure_city(), format),
            self.config.get_formatted_cities(format)
        )

    def get_date(self, offset: int=0):
        return super().get_date('%d.%m.%Y', offset)

    def search_location(self, parts: list, offset: int):
        search = self.session.get('https://global.api.flixbus.com/search/service/v4/search', params={
            'from_city_id': self.departure[2],
            'to_city_id': parts[2],
            'departure_date': self.get_date(offset),
            'products': '{"adult":1}',
            'currency': 'EUR',
            'locale': 'it',
            'search_by': 'cities',
            'include_after_midnight_rides': '1'
        }).json()

        if search.get('code') == 400:
            return

        for k in search.get('trips', [{}])[0].get('results', {}):
            _trip = search.get('trips')[0]['results'][k]
            price = _trip['price']['total']
            if price > 0 and price <= self.config.get('configuration', {}).get('price_cap', 20):
                self.trips.append(
                    Trip(
                        date=dateutil.parser.parse(_trip['departure']['date']),
                        departure=self.departure[0],
                        arrival=parts[0],
                        carrier=self.get_basename(),
                        duration=(_trip['duration']['hours'] * 60) + _trip['duration']['minutes'],
                        price=price,
                        arrival_country=parts[1]
                    )
                )
