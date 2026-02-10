from backend.populate import gtfs, model
import requests
import json

class Main(model.RouteFinder):
    FLIXBUS_EUROPE_URL = 'http://gtfs.gis.flix.tech/gtfs_generic_eu.zip'
    def __init__(self):
        super().__init__(True)
        self.g = gtfs.GTFS()
        self.g.import_from_url(self.FLIXBUS_EUROPE_URL)

    def get_route_by_number(self, number):
        for route in self.g.get('routes'):
            if route['route_id'] == number:
                return route
    
    def get_routes_by_place(self, place):
        routes = []
        for route in self.g.get('routes'):
            if place.lower() in route['route_long_name'].lower():
                routes.append(route)
        return routes
    
    def get_stop_by_id(self, id):
        for stop in self.g.get('stops'):
            if stop['stop_id'] == id:
                return stop

    def get_bus_stops(self, number):
        stops = []
        for stop in self.g.get('stop_times'):
            _number = stop['trip_id'].split('-')[0]
            if _number == number:
                stops.append(self.get_stop_by_id(stop['stop_id']))
        return stops

    def get_reachable_cities(self, place):
        cities = []
        for route in self.get_routes_by_place(place):
            stops = self.get_bus_stops(route['route_id'])[1:] # escludo la partenza
            for stop in stops:
                if not stop in cities:
                    cities.append(stop)
        return cities
    
    def get_reach(self, place):
        formatted = list()
        for stop in self.get_reachable_cities(place):
            formatted.append(model.Route(
                stop['stop_name'], 
                '', # non lo sappiamo
                stop['stop_id'], 
                stop['stop_lat'], 
                stop['stop_lon']
            ))
        return formatted
    
    def normalize(self, route): # gtfs stop id != flixbus place id (abbiamo bisogno di un match)
        place = requests.get('https://global.api.flixbus.com/cms/cities', params={
            'language': 'en',
            'limit': 1,
            'geo_bounding_box': json.dumps({
                'top_left': {
                    'lat': float(route.latitude) + 2e-2,
                    'lon': float(route.longitude) - 4e-2
                },
                'bottom_right': {
                    'lat': float(route.latitude) - 2e-2,
                    'lon': float(route.longitude) + 4e-2
                }
            }),
        }).json()
        results = place.get('result', [])
        if results:
            place = results[0]
            route.name = place.get('name')
            route.country = place.get('country')
            route.id = place.get('uuid')
        return route