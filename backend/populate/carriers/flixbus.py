from backend.populate import gtfs
import requests
import json

NORMALIZE = True
class Main:
    FLIXBUS_EUROPE_URL = 'http://gtfs.gis.flix.tech/gtfs_generic_eu.zip'
    def __init__(self):
        self.g = gtfs.GTFS()
        self.g.import_from_url(self.FLIXBUS_EUROPE_URL)

    def get_route_by_number(self, number):
        for route in self.g.get('routes'):
            if route['route_id'] == number:
                return route
    
    def get_routes_by_city(self, city):
        routes = []
        for route in self.g.get('routes'):
            if city.lower() in route['route_long_name'].lower():
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

    def get_reachable_cities(self, city):
        cities = []
        for route in self.get_routes_by_city(city):
            stops = self.get_bus_stops(route['route_id'])[1:] # escludo la partenza
            for stop in stops:
                if not stop in cities:
                    cities.append(stop)
        return cities
    
    def get_reach(self, city):
        formatted = []
        for stop in self.get_reachable_cities(city):
            formatted.append((stop['stop_name'], '', stop['stop_id'], (stop['stop_lat'], stop['stop_lon'])))
        return formatted
    
    def normalize(self, lat, lon): # gtfs stop id != flixbus city id (abbiamo bisogno di un match)
        lat, lon = float(lat), float(lon)
        city = requests.get('https://global.api.flixbus.com/cms/cities',
                   params={
                        'language': 'en',
                        'geo_bounding_box': json.dumps({
                            'top_left': {
                                'lat': lat + 2e-2,
                                'lon': lon - 4e-2
                            },
                            'bottom_right': {
                                'lat': lat - 2e-2,
                                'lon': lon + 4e-2
                            }
                        }),
                       'limit': 1,
                    }
                   ).json()
        if city.get('result'):
            city = city.get('result')[0]
            return (city.get('name'), city.get('country'), city.get('uuid'))