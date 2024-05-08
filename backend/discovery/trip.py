from backend import geocoding
import json

class Trip:
    date = None
    carrier = None
    departure = None
    arrival = None
    arrival_country = None
    duration = None
    price = None
    
    def __init__(self, date, departure, arrival, carrier, duration, price, arrival_country=None):
        self.date = date
        self.departure = departure
        self.arrival = arrival
        self.arrival_country = arrival_country
        self.carrier = carrier
        self.duration = duration
        self.price = price

    def __str__(self):
        return f'Trip({self.format_date()}, {self.format_time()}, {self.departure}, {self.arrival}, {self.arrival_country}, {self.carrier}, {self.format_duration()}, {self.format_price()})'

    def __repr__(self):
        return self.__str__()

    def format_duration(self):
        if self.duration % 60 == 0:
            return f'{int(self.duration/60)}h'
        total = self.duration/60
        hours = int(total)
        minutes = total - hours
        return f'{hours}h {round(minutes*60)}m'
    
    def format_date(self):
        return self.date.strftime('%d/%m')

    def format_time(self):
        return self.date.strftime('%H:%M')
    
    def format_price(self):
        return '{:0,.2f}'.format(self.price)
    
    def to_dict(self):
        return {
            'date': self.format_date(),
            'time': self.format_time(),
            'departure': self.departure,
            'arrival': self.arrival,
            'arrival_loc': geocoding.get_coordinates(f'{self.arrival}, {self.arrival_country}'),
            'arrival_country': self.arrival_country,
            'carrier': self.carrier,
            'duration': self.format_duration(),
            'price': self.price,
            'formatted_price': self.format_price()
        }

class TripEncoder(json.JSONEncoder):
    def default(self, trip):
        return trip.to_dict()