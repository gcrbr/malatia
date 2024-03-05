from backend.discovery import trip
from backend.http import handler
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
            print(f'<!> Avvio ricerca su \'{carrier.__name__}\'')
            for d in range(offset + 1):
                try:
                    trips += carrier.Main().search_trips(d)
                except:
                    pass
        trips.sort(key=lambda t: t['price'])
        file = open('data.json', 'w')
        file.write(json.dumps(trips))
        file.close()
        print(f'\n<!> {len(trips)} viaggi salvati su data.json')
        time.sleep(delay)

def run_http_server(port):
    http.server.HTTPServer(('localhost', port), handler.mHandler).serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--delay', help='Tempo in secondi tra ogni operazione di ricerca (default: 5 ore)', default=18000)
    parser.add_argument('-i', '--interface', help='Avvia un server HTTP per l\'interfaccia grafica (default: disabilitato)', action='store_true')
    parser.add_argument('-p', '--port', help='Porta del server HTTP dell\'interfaccia (default: 8000)', default=8000)
    parser.add_argument('-o', '--offset', help='Numero di giorni dopo la data corrente per il quale bisogna ricercare viaggi (es. "-o 2" = viaggi per domani e dopodomani, default: 3)', default=3)
    parser.add_argument('-c', '--carriers', help='Seleziona manualmente i vettori da includere (es. "-c itabus,flixbus", default: tutti)')
    parser.add_argument('-pc', '--pricecap', help='Imposta il prezzo massimo (default: 20)', default=20)
    parser.add_argument('-io', '--interfaceonly', help='Avvia solo l\'interfaccia, senza ricercare nuovi viaggi', action='store_true')

    args = parser.parse_args()

    print('MALATÌA <github.com/gcrbr>')
    
    if type(args.offset) is not int and not args.offset.isnumeric():
        print('\n<!> Valore invalido fornito per l\'offset')
        exit(1)
    
    if type(args.pricecap) is not int and not args.pricecap.isnumeric():
        print('\n<!> Valore invalido fornito per il price cap')
        exit(1)
    
    args.offset = int(args.offset)
    args.pricecap = int(args.pricecap)

    trip.good_price = args.pricecap

    carriers = []
    if args.carriers:
        ref = args.carriers.split(',')
    else:
        ref = [os.path.basename(f)[:-3] for f in glob.glob('backend/discovery/carriers/*.py')]
    
    for c in ref:
        try:
            carriers.append(__import__('backend.discovery.carriers.' + c, fromlist=[None]))
        except ImportError:
            print(f'\n<!> Il vettore \'{c}\' non è stato trovato')
            exit(1)

    if args.interface:
        import http.server
        threading.Thread(target=run_http_server, args=(args.port,)).start()
        print(f'Server HTTP attivo su localhost:{args.port}')
    
    print('')

    if not args.interfaceonly:
        threading.Thread(target=discovery_loop, args=(carriers, args.delay, int(args.offset),)).start()