from utils import Console
from backend import config
import datetime
import requests

class Discovery:
    ENABLED: bool = True
    EXTERNAL_OFFSET: bool = False
    _config = None

    @property
    def config(self):
        if Discovery._config is None:
            from backend.config import Config
            Discovery._config = Config()
        return Discovery._config

    def __init__(self, departure):
        self.session = requests.session()
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.departure = departure
        if not self.departure:
            Console.warning(f'[{self.get_basename()}] Unable to determine the departure city. Check that your config.json contains the necessary identifiers for this carrier.')
            self.search_trips = lambda *_: []
    
    @classmethod
    def get_basename(cls) -> str:
        return cls.__module__.split('.')[-1]

    def get_date(self, format, offset=0):
        return (datetime.datetime.now() + datetime.timedelta(offset)).strftime(format)

    def search_trips(self, offset=0):
        pass