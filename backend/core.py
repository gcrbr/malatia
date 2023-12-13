import flixbus
import ryanair
import time
import json

HOUR_INTERVAL = 5

def run_update_data():
    while 1:
        print('-> Saving trips...')
        trips = flixbus.search_trips(flixbus.departure, flixbus.arrivals) + ryanair.search_flights(ryanair.departure)
        file = open('../data.json', 'w')
        file.write(json.dumps(trips))
        file.close()
        print('-> OK')
        time.sleep(60 * 60 * HOUR_INTERVAL)

if __name__ == '__main__':
    print('@')
    run_update_data()