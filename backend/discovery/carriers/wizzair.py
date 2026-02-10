from backend.discovery import discovery
from backend.discovery import trip
import dateutil.parser
import utils
import re

class Main(discovery.Discovery):
    EXTERNAL_OFFSET = True
    ENABLED = True

    def __init__(self):
        super().__init__(self.config.get_departure_city().get('identifiers').get('wizzair'))
        self.exchange_rate = 0
        self.api_version = self.get_api_version()
        self.airport_data = self.session.get(f'https://be.wizzair.com/{self.api_version}/Api/asset/map?languageCode=en-gb').json()

    def get_api_version(self) -> str:
        response = self.session.get('https://wizzair.com').text
        match = re.search(r'apiUrl":"(.*?)"', response)
        if match:
            return match.group(1).split('\\u002F')[3]
        return None

    def currency_to_eur(self, currency, amount):
        if not self.exchange_rate:
            data = self.session.get(f'https://www.xe.com/api/protected/statistics/?from={currency}&to=EUR',
            headers={'authorization':'Basic bG9kZXN0YXI6cHVnc25heA=='}).json()
            self.exchange_rate = list(data.values())[0].get('average')
        return amount * self.exchange_rate
    
    def get_airport_name(self, iata):
        for airport in self.airport_data['cities']:
            if airport['iata'].lower() == iata.lower():
                return airport['aliases'][0]

    def get_date(self, offset=0):
        return super().get_date('%Y-%m-%d', offset)

    def search_trips(self, offset=0):
        trips = []
        search = self.session.post(f'https://be.wizzair.com/{self.api_version}/Api/search/SmartSearchCheapFlights', json={
            'arrivalStations': None,
            'departureStations': [self.departure],
            'tripDuration': 'anytime',
            'isReturnFlight': False,
            'stdPlan': None,
            'pax': 1,
            'dateFilterType': 'Exact',
            'departureDate': self.get_date(offset),
            'returnDate': None
        }).json()

        for flight in search.get('items', []):
            price = self.currency_to_eur(flight.get('currencyCode'), flight.get('regularPrice', {}).get('amount', 0))
            if price > 0 and price <= self.config.get('configuration', {}).get('price_cap', 20):
                trips.append(
                    trip.Trip(
                        date=dateutil.parser.parse(flight.get('std')),
                        departure=self.get_airport_name(self.departure),
                        arrival=self.get_airport_name(flight.get('arrivalStation')),
                        carrier=self.get_basename(),
                        duration=flight.get('flightDurationMinutes'),
                        price=price,
                        arrival_country=''
                    )
                )
        return trips