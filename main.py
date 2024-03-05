from backend.discovery import flixbus, ryanair, itabus
from backend.http import handler
import threading
import argparse
import time
import json

def discovery_loop(delay, offset):
    carriers = [flixbus, ryanair, itabus]
    while True:
        trips = []
        for carrier in carriers:
            print(f'<!> avvio ricerca su {carrier.__name__}')
            for d in range(offset + 1):
                try:
                    trips += carrier.search_trips(d)
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

    parser.add_argument('-d', '--delay', help='tempo in secondi tra ogni operazione di ricerca', default=18000)
    parser.add_argument('-i', '--interface', help='avvia un server HTTP per l\'interfaccia grafica', action='store_true')
    parser.add_argument('-p', '--port', help='porta del server HTTP dell\'interfaccia', default=8000)
    parser.add_argument('-o', '--offset', help='numero di giorni dopo la data corrente per il quale bisogna ricercare viaggi (es. 2=viaggi per domani e dopodomani)', default=3)

    args = parser.parse_args()

    print('MALATÌA <github.com/gcrbr>')
    
    if type(args.offset) is not int and not args.offset.isnumeric():
        print('<!> valore invalido fornito per l\'offset, sono ammessi solo valori interi')
        exit(1)
    
    args.offset = int(args.offset)

    if args.interface:
        import http.server
        threading.Thread(target=run_http_server, args=(args.port,)).start()
        print(f'server HTTP attivo su localhost:{args.port}')
    
    print('')

    threading.Thread(target=discovery_loop, args=(args.delay, int(args.offset),)).start()
        
    
            