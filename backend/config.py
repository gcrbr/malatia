import os.path
import utils
import json

class Config:
    def __init__(self):
        self.read_config_file()

    def set_default_config(self):
        self.config = {}

    def read_config_file(self):
        if not os.path.isfile('config.json'):
            self.set_default_config()
            return
        file = open('config.json')
        data = file.read()
        file.close()

        try:
            data = json.loads(data)
        except:
            self.set_default_config()
            return
        
        self.config = data

    def get_city(self, key, value):
        for city in self.config['cities']:
            if city.get(key).lower() == value.lower():
                return city

    def get_departure_city(self):
        dep_city = self.config.get('configuration').get('departure')
        if not (r := self.get_city('name', dep_city)):
            utils.err('Invalid departure city, please check your config file', True)
        return r
    
    def get_city_identifier(self, city, carrier):
        return self.get_city('name', city).get('identifiers').get(carrier)
    
    def get_cities(self):
        return self.config.get('cities')
    
    def format_city_object(self, city, format):
        _tuple = []
        for q in format:
            if not '.' in q:
                c = city.get(q)
            else:
                sub = q.split('.')
                c = city.get(sub[0])
                for dot in sub[1:]:
                    c = c.get(dot)
            _tuple.append(c)
            if c == None:
                return c
        return tuple(_tuple)

    def get_formatted_cities(self, format):
        formatted = []
        for city in self.get_cities():
            if city.get('name') == self.get_departure_city().get('name'):
                continue
            if f := self.format_city_object(city, format):
                formatted.append(f)
        return formatted