from backend.discovery import multidiscovery
from backend.discovery import trip
import dateutil.parser

EXTERNAL_OFFSET = True
ENABLED = True
class Main(multidiscovery.Multidiscovery):
    carriers = {
        '2468': 'trenitalia', # Frecciarossa,
        '1276': 'italo',
        '3139': 'trenitalia', # Intercity
        '3140': 'trenitalia', # Intercity notte,
    }
    def __init__(self):
        format = ('name', 'identifiers.omio')
        super().__init__(
            self.config.format_city_object(self.config.get_departure_city(), format),
            self.config.get_formatted_cities(format)
        )
    
    def get_date(self, offset=0):
        return super().get_date('%Y-%m-%d', offset)

    def search_location(self, p, offset):
        try:
            headers = {
                'user-agent': 'GoEuroIOS /9.17.1 (iPhone; iOS 17.2.1; Scale/3.00)',
                'goeuro-client': 'GoEuroIOS /9.17.1 (iPhone; iOS 17.2.1; Scale/3.00)'
            }
            search_init = self.session.post('https://www.omio.com/offline-search-api/rest/api//v5/searches', json=
                {'searchOptions': {
                    'departureDate': self.get_date(offset),
                    'departurePosition': {
                        'id': self.departure[1]
                    },
                    'passengers': [{
                        'discountCards': [],
                        'type': 'adult',
                        'age': 26,
                        'passengerAge': {
                            'min': 26,
                            'max': 57,
                            'age': 26
                        }
                    }],
                    'arrivalPosition': {
                        'id': p[1]
                    },
                    'travelModes': ['train'],
                    'userInfo': {
                        'identifier': '-',
                        'domain': 'com',
                        'locale': 'it',
                        'currency': 'EUR'
                    },
                    'includeRoutedConnections': True
                }
            }, headers=headers).json()

            search = {'query':{'searchModes':{'train':{'status':'inprogress'}}}}
            attempt = 0

            while search['query']['searchModes']['train']['status'] == 'inprogress' and attempt < 20: # 20 Refresh attempts
                search = self.session.get('https://www.omio.com/offline-search-api/rest/api/v5/results', params={
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

            for k, _trip in search['outbounds'].items():
                _trip = search['outbounds'][k]
                if _trip['companyId'] in self.carriers and len(_trip['segments']) == 1 and ((price := _trip['originalPrice']/100) <= self.config.config.get('configuration').get('price_cap') and price > 0):
                    self.trips.append(
                        trip.Trip(
                            date=dateutil.parser.isoparse(_trip['departureTime']),
                            departure=self.departure[0],
                            arrival=p[0],
                            carrier=self.carriers[_trip['companyId']],
                            duration=(dateutil.parser.isoparse(_trip['arrivalTime']) - dateutil.parser.isoparse(_trip['departureTime'])).seconds/60,
                            price=price,
                            arrival_country='Italy'
                        )
                    )
        except:
            pass

