import flixbus
import ryanair
import random
import time
import json

HOUR_INTERVAL = 5

def run_update_data():
    while 1:
        print('-> Saving trips...')
        trips = []
        for x in range(3): #domani, dopodomani, dopodopodomani
            trips += flixbus.search_trips(flixbus.departure, flixbus.arrivals, x) + ryanair.search_flights(ryanair.departure, x)
        trips.sort(key=lambda t: t['price'])
        file = open('../data.json', 'w')
        file.write(json.dumps(trips))
        file.close()
        print('-> OK')
        time.sleep(60 * 60 * HOUR_INTERVAL) #ogni ora

if __name__ == '__main__':
    print('@')
    run_update_data()