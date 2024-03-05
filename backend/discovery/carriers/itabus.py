from backend.discovery import multidiscovery
from backend.discovery import trip
import dateutil.parser
import requests
import os.path

class Main(multidiscovery.Multidiscovery):
    def __init__(self):
        super().__init__(
            ('Napoli', 'NAP_T'),
            [
                ('Milano', 'MIL_T'),
                ('Torino', 'TOR_T'),
                ('Roma', 'ROM_T'),
                ('Palermo', 'PAM_T'),
                ('Agrigento', 'AGR_T'),
                ('Aosta', 'AOT_T'),
                ('San Benedetto del Tronto', 'SBN_T'),
                ('L\'Aquila', 'LAQ_T'),
                ('Catania', 'CAT_T'),
                ('Firenze', 'FIR_T'),
                ('Venezia', 'VEN_T'),
                ('Bologna', 'BOL_T'),
                ('Bergamo', 'BGG_T'),
                ('Mantova', 'MAN_T'),
                ('Verona', 'VER_T'),
                ('Reggio Emilia', 'REG_T'),
                ('Bari', 'BAR_T')
            ]
        )

    def get_date(self, offset=0):
        return super().get_date('%Y-%m-%d', offset)

    def search_location(self, p, offset):
        try:
            search = requests.get(f'https://www.itabus.it/on/demandware.store/Sites-ITABUS-Site/it/Api-Travels?origin={self.departure[1]}&destination={p[1]}&datestart={self.get_date(offset)}&adults=1&children=0&membership=false').json()
            for _trip in search['data']['outbound']['routes']:
                if (price := _trip['bundles']['BASIC'][0]['price']) < trip.good_price and price > 0:
                    self.trips.append(
                        trip.Trip(
                            date=dateutil.parser.isoparse(_trip['departure_timestamp']),
                            departure=self.departure[0],
                            arrival=p[0],
                            carrier=self.base_name(__name__),
                            duration=(dateutil.parser.isoparse(_trip['arrival_timestamp']) - dateutil.parser.isoparse(_trip['departure_timestamp'])).seconds/60,
                            price=price,
                            arrival_country='Italy'
                        ).to_dict()
                    )
        except:
            pass