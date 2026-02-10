from backend.discovery import discovery
from backend.discovery.trip import Trip
import dateutil.parser

class Main(discovery.Discovery):
    EXTERNAL_OFFSET = False
    ENABLED = True

    def __init__(self):
        super().__init__(self.config.get_departure_city().get('identifiers').get('ryanair'))

    def get_date(self, offset: int=0):
        return super().get_date('%Y-%m-%d', offset)

    def search_trips(self, offset: int=0):
        trips = []
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

        for k in search.get('fares', []):
            flight = k.get('outbound', {})
            price = flight.get('price', {}).get('value', 0)
            if price > 0 and price <= self.config.get('configuration', {}).get('price_cap', 20):
                trips.append(
                    Trip(
                        date=dateutil.parser.parse(flight.get('departureDate', '')),
                        departure=self.departure,
                        arrival=flight.get('arrivalAirport', {}).get('city', {}).get('name', ''),
                        carrier=self.get_basename(),
                        duration=(dateutil.parser.parse(flight.get('arrivalDate', '')) - dateutil.parser.parse(flight.get('departureDate', ''))).seconds/60,
                        price=price,
                        arrival_country=flight.get('arrivalAirport', {}).get('countryName', '')
                    )
                )
        return trips