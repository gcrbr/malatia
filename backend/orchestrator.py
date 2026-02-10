import threading
import time
import json
import concurrent.futures
from utils import Console
from backend.discovery import trip
from backend.geocoding import Place

class DiscoveryOrchestrator:
    def __init__(self, carriers, delay, offset, data_file, geocoding_enabled=True):
        self.carriers = carriers
        self.delay = delay
        self.offset = offset
        self.data_file = data_file
        self.geocoding_enabled = geocoding_enabled
        self.is_running = True

    def geocode_trips(self, trips):
        if not self.geocoding_enabled:
            return

        Console.info(f'Geocoding {len(trips)} journeys...')
        start_time = time.time()
        
        # Get unique arrival locations
        unique_locations = {}
        for t in trips:
            loc = f'{t.arrival}, {t.arrival_country}'
            if loc not in unique_locations:
                unique_locations[loc] = []
            unique_locations[loc].append(t)

        def fetch_coords(loc_str):
            p = Place(loc_str)
            return loc_str, p.get_coordinates()

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_loc = {executor.submit(fetch_coords, loc): loc for loc in unique_locations}
            for future in concurrent.futures.as_completed(future_to_loc):
                loc_str, coords = future.result()
                for t in unique_locations[loc_str]:
                    t.coordinates = coords

        Console.info(f'Geocoding completed in {round(time.time() - start_time, 2)}s')

    def run(self):
        while self.is_running:
            all_trips = []
            for carrier_module in self.carriers:
                carrier_class = carrier_module.Main
                if not carrier_class.ENABLED:
                    continue
                
                # Check for departure availability (some carriers might not have it configured)
                try:
                    if not carrier_class().departure:
                        continue
                except:
                    continue

                start_time = time.time()
                Console.info(f'[{carrier_class.get_basename()}] Searching for journeys')
                
                prev_len = len(all_trips)
                days_to_search = self.offset + 1 if carrier_class.EXTERNAL_OFFSET else 1
                
                for d in range(days_to_search):
                    try:
                        search_offset = d if carrier_class.EXTERNAL_OFFSET else (self.offset + 1)
                        found_trips = carrier_class().search_trips(search_offset)
                        all_trips += found_trips
                    except Exception as e:
                        Console.err(f'[{carrier_class.get_basename()}] {e}')
                
                Console.info(f'[{carrier_class.get_basename()}] Found {len(all_trips) - prev_len} journeys in {round(time.time() - start_time, 2)}s')

            # Deduplicate or sort? deduplication might be useful if same trip found in different days or carriers
            all_trips.sort(key=lambda t: t.price)
            
            # Geocode unique locations in parallel
            self.geocode_trips(all_trips)

            # Save to file
            try:
                with open(self.data_file, 'w') as f:
                    f.write(json.dumps(all_trips, cls=trip.TripEncoder))
                Console.empty_line()
                Console.info(f'{len(all_trips)} journeys saved on {self.data_file}')
            except Exception as e:
                Console.err(f'Failed to save data: {e}')

            if self.delay <= 0:
                break
                
            Console.info(f'Next search in {self.delay}s...')
            time.sleep(self.delay)

    def stop(self):
        self.is_running = False