from backend.discovery import multidiscovery
from backend.discovery.trip import Trip
import dateutil.parser

class Main(multidiscovery.Multidiscovery):
    EXTERNAL_OFFSET = True
    ENABLED = True

    def __init__(self):
        format = ('name', 'identifiers.itabus')
        super().__init__(
            self.config.format_city_object(self.config.get_departure_city(), format),
            self.config.get_formatted_cities(format)
        )
        
    def get_date(self, offset: int=0):
        return super().get_date('%Y-%m-%d', offset)

    def search_location(self, parts: list, offset: int=0):
        search = self.session.get(f'https://www.itabus.it/on/demandware.store/Sites-ITABUS-Site/en/Api-Travels', params={
            'origin': self.departure[1],
            'destination': parts[1],
            'datestart': self.get_date(offset),
            'adults': 1,
            'children': 0,
            'membership': False
        })
        
        if search.status_code != 200:
            return

        for _trip in search.json().get('data', {}).get('outbound', {}).get('routes', []):
            bundles = sorted(list([j for j in _trip['bundles'].values() if j]),key=lambda x: x[0].get('price', float('inf')))
            price = bundles[0][0].get('price', -1)
            if price > 0 and price <= self.config.get('configuration', {}).get('price_cap', 20):
                self.trips.append(
                    Trip(
                        date=dateutil.parser.isoparse(_trip.get('departure_timestamp')),
                        departure=self.departure[0],
                        arrival=parts[0],
                        carrier=self.get_basename(),
                        duration=(dateutil.parser.isoparse(_trip.get('arrival_timestamp')) - dateutil.parser.isoparse(_trip.get('departure_timestamp'))).seconds/60,
                        price=price,
                        arrival_country='Italy'
                    )
                )