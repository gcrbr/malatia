from backend.discovery import discovery
from backend.discovery import trip
import dateutil.parser

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
                'outboundDepartureDateFrom': self.get_date(offset),
                'market': 'it',
                'adultPaxCount': '1',
                'outboundDepartureDateTo': self.get_date(offset),
                'outboundDepartureTimeFrom': '00:00',
                'outboundDepartureTimeTo': '23:59'
            }).json()
            for k in search['fares']:
                flight = k['outbound']
                if (price := flight['price']['value']) <= trip.good_price and price > 0:
                    trips.append(
                        trip.Trip(
                            date=dateutil.parser.parse(flight['departureDate']),
                            departure='Napoli',
                            arrival=flight['arrivalAirport']['city']['name'],
                            carrier=self.base_name(__name__),
                            duration=(dateutil.parser.parse(flight['arrivalDate'])-dateutil.parser.parse(flight['departureDate'])).seconds/60,
                            price=price,
                            arrival_country=flight['arrivalAirport']['countryName']
                        )
                    )
        except: 
            pass
        return trips