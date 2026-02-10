from backend.discovery import multidiscovery
from backend.discovery import trip
import dateutil.parser
import time

class Main(multidiscovery.Multidiscovery):
    EXTERNAL_OFFSET = True
    ENABLED = True

    carriers = {
        '3137': 'trenitalia', # Regionale,
        '2468': 'trenitalia', # Frecciarossa,
        '1276': 'italo',
        '3139': 'trenitalia', # Intercity
        '3140': 'trenitalia', # Intercity notte,
    }
    def __init__(self):
        self.api_name = 'GoEuroAPI'#'offline-search-api'
        format = ('name', 'identifiers.omio')
        super().__init__(
            self.config.format_city_object(self.config.get_departure_city(), format),
            self.config.get_formatted_cities(format)
        )
    
    def get_date(self, offset=0):
        return super().get_date('%Y-%m-%d', offset)

    def search_location(self, parts, offset):
        headers = {
            'user-agent': 'GoEuroIOS /9.17.1 (iPhone; iOS 17.2.1; Scale/3.00)',
            'goeuro-client': 'GoEuroIOS /9.17.1 (iPhone; iOS 17.2.1; Scale/3.00)'
        }
        search_init = self.session.post(f'https://www.omio.com/{self.api_name}/rest/api//v5/searches', json={'searchOptions': {
            'departureDate': self.get_date(offset),
            'departurePosition': {
                'id': self.departure[1]
            },
            'passengers': [{
                'discountCards': [],
                'type': 'adult',
                'age': 26,
                'passengerAge': {'min': 26, 'max': 57, 'age': 26}
            }],
            'arrivalPosition': {
                'id': parts[1]
            },
            'travelModes': ['train'],
            'userInfo': {
                'identifier': '-',
                'domain': 'com',
                'locale': 'en',
                'currency': 'EUR'
            },
            'includeRoutedConnections': True
        }}, headers=headers).json()

        search = {}
        attempt = 0

        if 'searchId' not in search_init:
            return

        while search.get('query', {}).get('searchModes', {}).get('train', {}).get('status', 'inprogress') == 'inprogress' and attempt < 20: # 20 Refresh attempts
            search = self.session.get(f'https://www.omio.com/{self.api_name}/rest/api/v5/results', params={
                'direction': 'outbound',
                'search_id': search_init['searchId'],
                'sort_by': 'updateTime',
                'include_segment_positions': 'true',
                'use_recommendation': 'true',
                'use_stats': 'true',
                'sort_variants': 'smart',
                'exclude_offsite_bus_results': 'true',
                'exclude_offsite_train_results': 'true',
                'updated_since': '0',
            }, headers=headers).json()
            attempt += 1
            time.sleep(0.5)

        for k, _trip in search.get('outbounds', {}).items():
            price = _trip.get('price', 0)/100
            if _trip.get('companyId') in self.carriers and len(_trip.get('segments', [])) == 1 and (price > 0 and price <= self.config.config.get('configuration').get('price_cap')):
                self.trips.append(
                    trip.Trip(
                        date=dateutil.parser.isoparse(_trip.get('departureTime', '')),
                        departure=self.departure[0],
                        arrival=parts[0],
                        carrier=self.carriers.get(_trip.get('companyId'), ''),
                        duration=(dateutil.parser.isoparse(_trip.get('arrivalTime', '')) - dateutil.parser.isoparse(_trip.get('departureTime', ''))).seconds/60,
                        price=price,
                        arrival_country='Italy'
                    )
                )

