from backend import flixbus, ryanair
import threading
import argparse
import time

def discovery_loop(delay):
    carriers = [flixbus, ryanair]
    while True:
        trips = []
        for carrier in carriers:
            print(f'# Ricerca viaggi @ [{carrier.__name__}]')
            trips += carrier.search_trips()
        print(f'# {len(trips)} viaggi salvati su data.json')
        time.sleep(delay)

def run_http_server(port):
    http.server.HTTPServer(('localhost', port), http.server.SimpleHTTPRequestHandler).serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--delay', help='Tempo in secondi tra ogni operazione di ricerca', default=18000)
    parser.add_argument('-i', '--interface', help='Avvia un server HTTP per l\'interfaccia grafica', action='store_true')
    parser.add_argument('-p', '--port', help='Porta del server HTTP dell\'interfaccia', default=8000)

    args = parser.parse_args()

    print('Malatìa @ https://github.com/gcrbr/malatia')
    
    if args.interface:
        import http.server
        threading.Thread(target=run_http_server, args=(args.port,)).start()
        print(f'Server HTTP attivo su http://localhost:{args.port}')
    
    print('')

    threading.Thread(target=discovery_loop, args=(args.delay,)).start()
        
    
            