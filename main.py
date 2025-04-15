from backend.discovery import trip
from backend.http import handler
from backend import config
import threading
import colorama
import argparse
import os.path
import utils
import glob
import time
import json
import sys

data_file = 'data.json'

def discovery_loop(carriers, delay, offset):
    while True:
        trips = []
        for carrier in carriers:
            if not carrier.ENABLED:
                continue
            start_time = time.time()
            announce = f'{colorama.Fore.GREEN}(!) Searching for journeys on \'{carrier.__name__}\''
            sys.stdout.write(announce + '\r')
            _offset = 1
            if carrier.EXTERNAL_OFFSET:
                _offset = offset + 1
            for d in range(_offset):
                try:
                    trips += carrier.Main().search_trips(d if carrier.EXTERNAL_OFFSET else (offset + 1))
                except Exception as e:
                    print(f'[Error][{carrier}] {e}')
            sys.stdout.write(f'{announce} ({round(time.time() - start_time, 2)}s){colorama.Style.RESET_ALL}\n')
        trips.sort(key=lambda t: t.price)
        file = open(data_file, 'w')
        file.write(json.dumps(trips, cls=trip.TripEncoder))
        file.close()
        print(f'\n{colorama.Fore.YELLOW}(!) {len(trips)} journeys saved on {data_file}{colorama.Style.RESET_ALL}')
        time.sleep(delay)

def run_http_server(port):
    http.server.HTTPServer(('localhost', port), handler.mHandler).serve_forever()

if __name__ == '__main__':
    conf = config.Config()

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--interface', help='Runs an HTTP server for the graphical interface (default: disabled)', action='store_true')
    parser.add_argument('-p', '--port', help='Sets the port for the HTTP server (default: 8000)', default=8000)
    parser.add_argument('-o', '--offset', help='Number of days after the current date for which journeys need to be searched (default: 3)', default=3)
    parser.add_argument('-c', '--carriers', help='Manually select the carriers to research journeys on, separated by a comma (es. "-c itabus,flixbus", default: all)')
    parser.add_argument('-io', '--interfaceonly', help='Only runs the interface, without looking for new journeys', action='store_true')
    parser.add_argument('-ng', '--no-geocoding', help='Disable geocoding for faster search (the map will not work)', action='store_true')

    args = parser.parse_args()

    utils.print_intro()
    
    if type(args.offset) is not int and not args.offset.isnumeric():
        utils.err('Invalid value provided for \'offset\'', True)
    
    if type(args.port) is not int and not args.port.isnumeric():
       utils.err('Invalid value provided for \'port\'', True)
    
    args.port = int(args.port)
    
    args.offset = int(args.offset)

    price_cap = conf.config.get('configuration').get('price_cap')
    if not price_cap:
        price_cap = 20
        conf.config['configuration']['price_cap'] = price_cap

    delay = conf.config.get('configuration').get('delay')
    if not delay:
        delay = 18000
        conf.config['configuration']['delay'] = delay

    carriers = []
    if args.carriers:
        ref = [c.strip() for c in args.carriers.split(',')]
    else:
        ref = utils.get_source_files('backend.discovery.carriers')
    
    for c in ref:
        try:
            carriers.append(__import__('backend.discovery.carriers.' + c, fromlist=[None]))
        except ImportError:
            utils.err('Could not find the carrier \'{c}\'', True)

    if args.no_geocoding:
        trip.GEOCODING = False

    if args.interface or args.interfaceonly:
        import http.server
        threading.Thread(target=run_http_server, args=(args.port,)).start()
        print(f'{colorama.Fore.YELLOW}HTTP Server running on localhost:{args.port}{colorama.Style.RESET_ALL}')
    
    print('')

    if not args.interfaceonly:
        threading.Thread(target=discovery_loop, args=(carriers, delay, int(args.offset),)).start()