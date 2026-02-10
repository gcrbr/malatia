from backend.populate import model
import requests
import difflib

class Main(model.RouteFinder):
    def __init__(self):
        super().__init__(False)
        self.stations = requests.get(
            'https://www.itabus.it/on/demandware.store/Sites-ITABUS-Site/en/Api-Stations',
            headers={
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/100.0.1185.39'
            }
        ).json().get('data')
    
    def get_code_from_place(self, place):
        candidates = []
        for station in self.stations:
            place_name = station.get('name').lower()
            candidates.append((
                place_name,
                station.get('code'),
                difflib.SequenceMatcher(None, place.lower(), place_name).ratio()
            ))
        return max(candidates, key=lambda t:t[2])[1]
    
    def get_place_from_code(self, code):
        for station in self.stations:
            if station.get('code').lower() == code.lower():
                return station
    
    def get_reach(self, place):
        formatted = []
        reach = requests.get(
            'https://www.itabus.it/on/demandware.store/Sites-ITABUS-Site/en/Api-Station',
            params={'stationID': self.get_code_from_place(place)},
            headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/100.0.1185.39'}
        ).json()

        filtered_destinations = []
        check = dict()

        for d in reach.get('data').get('destinations'):
            d = self.get_place_from_code(d)
            if not d.get('place') in check:
                check[d.get('place')] = [d]
            else:
                check[d.get('place')].append(d)

        for x in check: # tra i doppioni (es. FIR2 e FIR_T, scelgo quello col _)
            x = check[x]
            if len(x) == 1:
                filtered_destinations.append(x[0])
            else:
                i = False
                for k in x:
                    if '_' in k.get('code'):
                        i = True
                        filtered_destinations.append(k)
                if not i:
                    filtered_destinations.append(x[0])

        filtered_destinations.append(
            self.get_place_from_code(self.get_code_from_place(place))
        ) # per la departure nella config

        for destination in filtered_destinations:
            stop = self.get_place_from_code(destination.get('code'))
            formatted.append(model.Route(
                stop.get('name'),
                'Italy',
                stop.get('code'),
                stop.get('coords').get('lat'),
                stop.get('coords').get('lng')
            ))
        return formatted