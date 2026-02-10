from backend.populate import model
from backend.geocoding import Place
import requests
import difflib
import re

class Main(model.RouteFinder):
    def __init__(self):
        super().__init__(False)
    
    def get_api_version(self) -> str:
        response = requests.get('https://wizzair.com').text
        match = re.search(r'apiUrl":"(.*?)"', response)
        if match:
            return match.group(1).split('\\u002F')[3]
        return None
    
    def get_reach(self, place: str):
        candidates = []
        airports = requests.get(f'https://be.wizzair.com/{self.get_api_version()}/Api/asset/map?languageCode=en-gb').json()
        for airport in airports.get('cities', []):
            candidates.append((
                airport.get('shortName'),
                airport.get('iata'),
                airport.get('countryName'),
                difflib.SequenceMatcher(None, place.lower(), airport.get('shortName').lower()).ratio()
            ))
        closest = max(candidates, key=lambda t: t[3])
        place = Place(f'{closest[0]} ({closest[1]})')
        lat, lon = place.get_coordinates()
        route = model.Route(
            closest[0],
            closest[2],
            closest[1],
            lat, lon
        )
        return [route]