from backend.discovery import trip
from backend.http import handler
from backend import config
import threading
import argparse
import os.path
import glob
import time
import json

def discovery_loop(carriers, delay, offset):
    while True:
        trips = []
        for carrier in carriers:
            print(f'(!) Avvio ricerca su \'{carrier.__name__}\'')
            for d in range(offset + 1):
                try:
                    trips += carrier.Main().search_trips(d)
                except:
                    pass
        trips.sort(key=lambda t: t['price'])
        file = open('data.json', 'w')
        file.write(json.dumps(trips))
        file.close()
        print(f'\n(!) {len(trips)} viaggi salvati su data.json')
        time.sleep(delay)

def run_http_server(port):
    http.server.HTTPServer(('localhost', port), handler.mHandler).serve_forever()

if __name__ == '__main__':
    c = config.Config()

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--interface', help='Avvia un server HTTP per l\'interfaccia grafica (default: disabilitato)', action='store_true')
    parser.add_argument('-p', '--port', help='Porta del server HTTP dell\'interfaccia (default: 8000)', default=8000)
    parser.add_argument('-o', '--offset', help='Numero di giorni dopo la data corrente per il quale bisogna ricercare viaggi (es. "-o 2" = viaggi per domani e dopodomani, default: 3)', default=3)
    parser.add_argument('-c', '--carriers', help='Seleziona manualmente i vettori da includere (es. "-c itabus,flixbus", default: tutti)')
    parser.add_argument('-io', '--interfaceonly', help='Avvia solo l\'interfaccia, senza ricercare nuovi viaggi', action='store_true')

    args = parser.parse_args()

    print('MALATÌA <github.com/gcrbr>')
    
    if type(args.offset) is not int and not args.offset.isnumeric():
        print('\n(!) Valore invalido fornito per l\'offset')
        exit(1)
    
    if type(args.port) is not int and not args.port.isnumeric():
        print('\n(!) Valore invalido fornito per la porta del server')
        exit(1)
    
    args.port = int(args.port)
    
    args.offset = int(args.offset)

    price_cap = c.config.get('configuration').get('price_cap')
    if not price_cap:
        price_cap = 20
    trip.good_price = price_cap

    delay = c.config.get('configuration').get('delay')
    if not delay:
        delay = 18000

    carriers = []
    if args.carriers:
        ref = args.carriers.split(',')
    else:
        ref = [os.path.basename(f)[:-3] for f in glob.glob('backend/discovery/carriers/*.py')]
    
    for c in ref:
        try:
            carriers.append(__import__('backend.discovery.carriers.' + c, fromlist=[None]))
        except ImportError:
            print(f'\n(!) Il vettore \'{c}\' non è stato trovato')
            exit(1)

    if args.interface or args.interfaceonly:
        import http.server
        threading.Thread(target=run_http_server, args=(args.port,)).start()
        print(f'Server HTTP attivo su localhost:{args.port}')
    
    print('')

    if not args.interfaceonly:
        threading.Thread(target=discovery_loop, args=(carriers, delay, int(args.offset),)).start()