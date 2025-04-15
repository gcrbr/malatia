from backend.discovery import discovery
from backend.discovery import trip
import dateutil.parser
import utils

EXTERNAL_OFFSET = True
ENABLED = True
class Main(discovery.Discovery):
    def __init__(self):
        super().__init__(self.config.get_departure_city().get('identifiers').get('wizzair'))
        self.exchange_rate = 0
        self.airport_data = self.session.get('https://be.wizzair.com/27.7.0/Api/asset/map?languageCode=en-gb').json()

    def currency_to_eur(self, currency, amount):
        if not self.exchange_rate:
            data = self.session.get(f'https://www.xe.com/api/protected/statistics/?from={currency}&to=EUR',
            headers={'authorization':'Basic bG9kZXN0YXI6cHVnc25heA=='}).json()
            self.exchange_rate = data.get('last1Days').get('average')
        return amount * self.exchange_rate
    
    def get_airport_name(self, iata):
        for airport in self.airport_data['cities']:
            if airport['iata'].lower() == iata.lower():
                return airport['aliases'][0]

    def get_date(self, offset=0):
        return super().get_date('%Y-%m-%d', offset)

    def search_trips(self, offset=0):
        trips = []
        try:
            search = self.session.post('https://be.wizzair.com/27.7.0/Api/search/SmartSearchCheapFlights',
            json={
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

            if not 'items' in search:
                return []

            for flight in search['items']:
                price = self.currency_to_eur(flight['currencyCode'], flight['regularPrice']['amount'])
                if price <= self.config.config.get('configuration').get('price_cap') and price > 0:
                    trips.append(
                        trip.Trip(
                            date=dateutil.parser.parse(flight['std']),
                            departure=self.get_airport_name(self.departure),
                            arrival=self.get_airport_name(flight['arrivalStation']),
                            carrier=self.base_name(__name__),
                            duration=flight['flightDurationMinutes'],
                            price=price,
                            arrival_country=''
                        )
                    )
        except Exception as e: 
            utils.err(f'[{__name__}]: {e}')
            pass
        return trips