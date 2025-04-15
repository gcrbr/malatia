import requests
import json

class Route:
    def __init__(self, name, country, id, latitude, longitude):
        self.name = name
        self.country = country
        self.id = id
        try:
            self.latitude = float(latitude)
            self.longitude = float(longitude)
        except:
            self.latitude = latitude
            self.longitude = longitude
    
    def __str__(self):
        return f'Route(name=\'{self.name}\', country=\'{self.country}\', id={self.id}, latitude={self.latitude}, longitude={self.longitude})'

class RouteEncoder(json.JSONEncoder):
    def default(self, route):
        return {
            'name': route.name,
            'country': route.country,
            'identifiers': {
                route.carrier: route.id
            }
        }

class RouteFinder:
    def __init__(self, normalization):
        self.normalization = normalization

    def get_reach(self, place: str) -> list[Route]:
        pass

    def normalize(self, route: Route) -> Route:
        pass