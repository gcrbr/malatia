import requests
import difflib

NORMALIZE = False
class Main:
    def __init__(self):
        self.stations = requests.get(
            'https://www.itabus.it/on/demandware.store/Sites-ITABUS-Site/it/Api-Stations',
            headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/100.0.1185.39'}
        ).json().get('data')
    
    def get_code_from_city(self, city):
        candidates = []
        for station in self.stations:
            city_name = station.get('name').lower()
            candidates.append((
                city_name,
                station.get('code'),
                difflib.SequenceMatcher(None, city.lower(), city_name).ratio()
            ))
        return max(candidates, key=lambda t:t[2])[1]
    
    def get_city_from_code(self, code):
        for station in self.stations:
            if station.get('code').lower() == code.lower():
                return station
    
    def get_reach(self, city):
        formatted = []
        reach = requests.get(
            'https://www.itabus.it/on/demandware.store/Sites-ITABUS-Site/it/Api-Station',
            params={'stationID': self.get_code_from_city(city)},
            headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/100.0.1185.39'}
        ).json()

        destinations = reach.get('data').get('destinations')
        _destinations = []
        check = {}

        for d in destinations:
            d = self.get_city_from_code(d)
            if not d.get('city') in check:
                check[d.get('city')] = [d]
            else:
                check[d.get('city')].append(d)

        for x in check: # tra i doppioni (es. FIR2 e FIR_T, scelgo quello col _)
            x = check[x]
            if len(x) == 1:
                _destinations.append(x[0])
            else:
                i = False
                for k in x:
                    if '_' in k.get('code'):
                        i = True
                        _destinations.append(k)
                if not i:
                    _destinations.append(x[0])

        _destinations.append(
            self.get_city_from_code(self.get_code_from_city(city))
        ) # per la departure nella config

        for destination in _destinations:
            stop = self.get_city_from_code(destination.get('code'))
            formatted.append((
                stop.get('name'),
                'Italy',
                stop.get('code'),
                (
                    stop.get('coords').get('lat'),
                    stop.get('coords').get('lng')
                )
            ))
        return formatted