import os.path
import json

class Config:
    def __init__(self):
        self.read_config_file()

    def set_default_config(self):
        self.config = {
            'configuration': {
                'departure': 'Napoli'
            },
            'cities': [
                {
                    'name': 'Napoli',
                    'country': 'Italy',
                    'identifiers': {
                        'flixbus': '40e096c1-8646-11e6-9066-549f350fcb0c',
                        'itabus': 'NAP_T',
                        'ryanair': 'NAP'
                    }
                },
                {
                    'name': 'Roma',
                    'country': 'Italy',
                    'identifiers': {
                        'flixbus': '40de90ff-8646-11e6-9066-549f350fcb0c',
                        'itabus': 'ROM_T'
                    }
                }
            ]
        }

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
        return self.get_city('name', dep_city)
    
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
            if not c:
                return None
            _tuple.append(c)
        return tuple(_tuple)

    def get_formatted_cities(self, format):
        formatted = []
        for city in self.get_cities():
            if city.get('name') == self.get_departure_city().get('name'):
                continue
            if f := self.format_city_object(city, format):
                formatted.append(f)
        return formatted