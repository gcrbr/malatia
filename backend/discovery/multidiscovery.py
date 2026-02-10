from backend.discovery import discovery
from concurrent.futures import ThreadPoolExecutor

class Multidiscovery(discovery.Discovery):
    def __init__(self, departure, arrivals):
        super().__init__(departure)
        self.arrivals = arrivals
        self.trips = []
    
    def search_location(self, place: str, offset: int):
        pass

    def search_trips(self, offset: int=0):
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(lambda p: self.search_location(p, offset), self.arrivals)
        return self.trips