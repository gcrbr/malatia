from backend.discovery import multidiscovery
from backend.discovery import trip
import dateutil.parser
import datetime
import json
import time

EXTERNAL_OFFSET = True
ENABLED = False
DELAY = 1
class Main(multidiscovery.Multidiscovery):
    def __init__(self):
        format = ('name', 'identifiers.trenitalia')
        super().__init__(
            self.config.format_city_object(self.config.get_departure_city(), format),
            self.config.get_formatted_cities(format)
        )
    
    def get_date(self, offset):
        now = datetime.datetime.now()
        return (datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(offset)).isoformat()

    def search_location(self, p, offset):
        search_data = {
            'departureLocationId': int(self.departure[1]),
            'arrivalLocationId': int(p[1]),
            'departureTime': self.get_date(offset),
            'adults': 1,
            'children': 0,
            'criteria': {
                'frecceOnly': True,
                'regionalOnly': False,
                'intercityOnly': False,
                'noChanges': True,
                'order': 'DEPARTURE_DATE',
                'offset': 0,
                'limit': 30,
            },
            'advancedSearchRequest': {
                'bestFare': False,
                'bikeFilter': False
            }
        }
        try:
            search_frecce = self.session.get('https://www.lefrecce.it/Channels.Website.BFF.WEB/website/ticket/solutions', json=search_data).text
            if 'Access Denied' in search_frecce: # Trenitalia does rate-limit requests
                return
            search_frecce = json.loads(search_frecce)
            search_data['criteria']['frecceOnly'] = False
            search_data['criteria']['intercityOnly'] = True
            search_intercity = self.session.get('https://www.lefrecce.it/Channels.Website.BFF.WEB/website/ticket/solutions', json=search_data).text
            if 'Access Denied' in search_intercity:
                return
            search_intercity = json.loads(search_intercity)
            solutions = search_frecce['solutions'] + search_intercity['solutions']
            for _trip in solutions:
                    if (price := _trip['solution']['price']['amount']) <= self.config.config.get('configuration').get('price_cap') and price > 0:
                        self.trips.append(
                            trip.Trip(
                                date=dateutil.parser.isoparse(_trip['departureTime']),
                                departure=self.departure[0],
                                arrival=p[0],
                                carrier=self.base_name(__name__),
                                duration=(dateutil.parser.isoparse(_trip['arrivalTime']) - dateutil.parser.isoparse(_trip['departureTime'])).seconds/60,
                                price=price,
                                arrival_country='Italy'
                            )
                        )
        except:
            pass
        time.sleep(DELAY) # Needed for rate-limiting