from backend.discovery import multidiscovery
from backend.discovery import trip
import dateutil.parser

EXTERNAL_OFFSET = True
ENABLED = True
class Main(multidiscovery.Multidiscovery):
    def __init__(self):
        format = ('name', 'identifiers.itabus')
        super().__init__(
            self.config.format_city_object(self.config.get_departure_city(), format),
            self.config.get_formatted_cities(format)
        )

    def get_date(self, offset=0):
        return super().get_date('%Y-%m-%d', offset)

    def search_location(self, p, offset):
        try:
            search = self.session.get(f'https://www.itabus.it/on/demandware.store/Sites-ITABUS-Site/it/Api-Travels?origin={self.departure[1]}&destination={p[1]}&datestart={self.get_date(offset)}&adults=1&children=0&membership=false').json()
            for _trip in search['data']['outbound']['routes']:
                if (price := _trip['bundles']['BASIC'][0]['price']) <= self.config.config.get('configuration').get('price_cap') and price > 0:
                    self.trips.append(
                        trip.Trip(
                            date=dateutil.parser.isoparse(_trip['departure_timestamp']),
                            departure=self.departure[0],
                            arrival=p[0],
                            carrier=self.base_name(__name__),
                            duration=(dateutil.parser.isoparse(_trip['arrival_timestamp']) - dateutil.parser.isoparse(_trip['departure_timestamp'])).seconds/60,
                            price=price,
                            arrival_country='Italy'
                        )
                    )
        except:
            pass