from backend.populate import model
from backend.geocoding import Place
import requests
import difflib

class Main(model.RouteFinder):
    def __init__(self):
        super().__init__(False)
    
    def get_reach(self, place: str):
        candidates = []
        airports = requests.get('https://www.ryanair.com/api/views/locate/5/airports/en/active').json()
        for airport in airports:
            candidates.append((
                airport.get('name'),
                airport.get('code'),
                difflib.SequenceMatcher(None, place.lower(), airport.get('name').lower()).ratio()
            ))
        closest = max(candidates, key=lambda t: t[2])
        place = Place(f'{closest[0]} ({closest[1]})')
        lat, lon = place.get_coordinates()
        route = model.Route(
            closest[0],
            '',
            closest[1],
            lat, lon
        )
        return [route]