from backend.populate import model
from backend.geocoding import Place
import requests
import difflib

class Main(model.RouteFinder):
    def __init__(self):
        super().__init__(False)
    
    def get_departure(self, place: str) -> model.Route:
        response = requests.get(f'https://www.omio.com/suggester-api/v5/position', params={
            'term': place,
            'locale': 'en',
            'hierarchical': 'true',
            'reduceResponse': 'true'
        }, headers={
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'GoEuroIOS /9.78.0 (iPhone; iOS 18.5; Scale/3.00)'
        }).json()
        first = response[0]
        lat, lon = first.get('latitude', 0), first.get('longitude', 0)
        locId = first.get('positionId')
        if first.get('children', []):
            locId = first['children'][0].get('positionId')
        route = model.Route(
            first.get('displayName'),
            first.get('countryNameInUserLocale'),
            locId,
            lat, lon
        )
        return route

    def get_reach(self, place: str) -> list[model.Route]:
        departure = self.get_departure(place)
        output = []
        response = requests.get(f'https://www.omio.com/suggester-api/v5/position/destination', params={
            'id': departure.id,
            'locale': 'en',
            'limit': '100'
        }, headers={
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'GoEuroIOS /9.78.0 (iPhone; iOS 18.5; Scale/3.00)'
        }).json()
        for item in response:
            output.append(model.Route(
                item.get('displayName'),
                item.get('countryNameInUserLocale'),
                item.get('positionId'),
                item.get('latitude', 0), item.get('longitude', 0)
            ))
        return [departure] + output
        