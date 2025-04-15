from backend.discovery import discovery
from backend.discovery import trip
import dateutil.parser
import utils

EXTERNAL_OFFSET = False
ENABLED = True
class Main(discovery.Discovery):
    def __init__(self):
        super().__init__(self.config.get_departure_city().get('identifiers').get('ryanair'))

    def get_date(self, offset=0):
        return super().get_date('%Y-%m-%d', offset)

    def search_trips(self, offset=0):
        trips = []
        try:
            search = self.session.get('https://www.ryanair.com/api/farfnd/v4/oneWayFares',
            params={
                'departureAirportIataCode': self.departure,
                'outboundDepartureDateFrom': self.get_date(0),
                'market': 'it',
                'adultPaxCount': '1',
                'outboundDepartureDateTo': self.get_date(offset),
                'outboundDepartureTimeFrom': '00:00',
                'outboundDepartureTimeTo': '23:59'
            }).json()

            if not 'fares' in search:
                return []

            for k in search['fares']:
                flight = k['outbound']
                if (price := flight['price']['value']) <= self.config.config.get('configuration').get('price_cap') and price > 0:
                    trips.append(
                        trip.Trip(
                            date=dateutil.parser.parse(flight['departureDate']),
                            departure=self.departure,
                            arrival=flight['arrivalAirport']['city']['name'],
                            carrier=self.base_name(__name__),
                            duration=(dateutil.parser.parse(flight['arrivalDate'])-dateutil.parser.parse(flight['departureDate'])).seconds/60,
                            price=price,
                            arrival_country=flight['arrivalAirport']['countryName']
                        )
                    )
        except Exception as e: 
            #utils.err(f'[{__name__}]: {e}')
            pass
        return trips