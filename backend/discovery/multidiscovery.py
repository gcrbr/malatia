from backend.discovery import discovery
import threading

class Multidiscovery(discovery.Discovery):
    def __init__(self, departure, arrivals):
        super().__init__(departure)
        self.arrivals = arrivals
        self.trips = []
    
    def search_location(self, p, offset):
        pass

    def search_trips(self, offset=0):
        threads = []
        for p in self.arrivals:
            if not p:
                continue
            thread = threading.Thread(target=self.search_location, args=(p, offset,))
            threads.append(thread)
            thread.start()
        for t in threads:
            t.join()
        return self.trips