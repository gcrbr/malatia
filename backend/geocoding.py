import requests
import threading

class Place:
    _coordinates = {}
    _countries = {}
    _lock = threading.Lock()

    def __init__(self, identifier: str):
        self.identifier = identifier.lower()
    
    def api_call(self, query: str) -> dict[str, str]:
        try:
            return requests.get('https://www.waze.com/live-map/api/autocomplete', 
                params={
                    'q': query,
                    'exp': '0,0,0',
                    'geo-env': 'row',
                    'v': '0,0;0,0', 
                    'lang': 'it'
                },
                headers={
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/100.0.1185.39'
                }
            ).json()
        except:
            return []
    
    def get_coordinates(self) -> tuple[float, float]:
        with Place._lock:
            if self.identifier in Place._coordinates:
                return Place._coordinates[self.identifier]
        
        lat, lon = 0, 0
        try:
            response = self.api_call(self.identifier)
            if len(response) < 1:
                return lat, lon
            found = response[0]
            lat, lon = float(found['latLng']['lat']), float(found['latLng']['lng'])
            
            with Place._lock:
                Place._coordinates[self.identifier] = (lat, lon)
        except:
            pass
        return lat, lon
    
    def get_country(self) -> str:
        with Place._lock:
            if self.identifier in Place._countries:
                return Place._countries[self.identifier]
        
        country = ''
        try:
            response = self.api_call(self.identifier)
            if len(response) < 1:
                return country
            found = response[0]
            country = found['address'].split(', ')[-1]
            
            with Place._lock:
                Place._countries[self.identifier] = country
        except:
            pass
        return country