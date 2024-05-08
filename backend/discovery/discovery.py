from backend import config
import datetime
import requests

class Discovery:
    session = requests.session()
    session.headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    config = config.Config()

    def __init__(self, departure):
        self.departure = departure
    
    def get_date(self, format, offset=0):
        return (datetime.datetime.now() + datetime.timedelta(offset)).strftime(format)

    def search_trips(self, offset=0):
        pass

    def base_name(self, name):
        return name.split('.')[-1]