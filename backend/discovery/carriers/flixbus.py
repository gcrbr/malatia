from backend.discovery import multidiscovery
from backend.discovery import trip
import dateutil.parser
import requests

class Main(multidiscovery.Multidiscovery):
    def __init__(self):
        super().__init__(
            ('Napoli', 'Italy', '40e096c1-8646-11e6-9066-549f350fcb0c'),
            [
                ('Roma', 'Italy', '40de90ff-8646-11e6-9066-549f350fcb0c'),
                ('Firenze', 'Italy', '40de71c6-8646-11e6-9066-549f350fcb0c'),
                ('Venezia', 'Italy', '40dea03b-8646-11e6-9066-549f350fcb0c'),
                ('Bari', 'Italy', '40df3bba-8646-11e6-9066-549f350fcb0c'),
                ('Pescara', 'Italy', '40df3966-8646-11e6-9066-549f350fcb0c'),
                ('Milano', 'Italy', '40ddcc6e-8646-11e6-9066-549f350fcb0c'),
                ('Trieste', 'Italy', '40de9f2f-8646-11e6-9066-549f350fcb0c'),
                ('Aosta', 'Italy', '40e2b92f-8646-11e6-9066-549f350fcb0c'),
                ('Bologna', 'Italy', '40df3653-8646-11e6-9066-549f350fcb0c'),
                ('Torino', 'Italy', '40deee02-8646-11e6-9066-549f350fcb0c'),

                ('Rijeka', 'Croatia', '40e11860-8646-11e6-9066-549f350fcb0c'),
                ('Zagreb', 'Croatia', '40dea87d-8646-11e6-9066-549f350fcb0c'),
                ('Lyon', 'France', '40df89c1-8646-11e6-9066-549f350fcb0c'),
                ('Budapest', 'Hungary', '40de6527-8646-11e6-9066-549f350fcb0c'),
                ('Geneva Airport', 'Switzerland', '89b7ebc7-cf52-4dac-97fd-b08ef8679623'),
                ('Münich', 'Germany', '40d901a5-8646-11e6-9066-549f350fcb0c'),
                ('Bern', 'Switzerland', '40df4ec8-8646-11e6-9066-549f350fcb0c'),
                ('Innsbrück', 'Austria', '40dd9a2a-8646-11e6-9066-549f350fcb0c'),
                ('Graz', 'Austria', '40de3c97-8646-11e6-9066-549f350fcb0c'),
                ('Cannes', 'France', '40e0010f-8646-11e6-9066-549f350fcb0c')
            ]
        )

    def get_date(self, offset=0):
        return super().get_date('%d.%m.%Y', offset)

    def search_location(self, p, offset):
        try:
            search = requests.get('https://global.api.flixbus.com/search/service/v4/search',
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
                if (price := _trip['price']['total']) < trip.good_price and price > 0:
                    self.trips.append(
                        trip.Trip(
                            date=dateutil.parser.parse(_trip['departure']['date']),
                            departure=self.departure[0],
                            arrival=p[0],
                            carrier=self.base_name(__name__),
                            duration=(_trip['duration']['hours'] * 60) + _trip['duration']['minutes'],
                            price=price,
                            arrival_country=p[1]
                        ).to_dict()
                    )
        except:
            pass