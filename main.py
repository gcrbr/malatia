from backend.discovery import trip
from backend.http import handler
from backend import config
from backend.orchestrator import DiscoveryOrchestrator
import threading
import argparse
import time
import json
from utils import Console, Files
import http.server
import sys

data_file = 'data.json'

def run_http_server(port):
    try:
        server = http.server.HTTPServer(('0.0.0.0', port), handler.mHandler)
        server.serve_forever()
    except Exception as e:
        Console.err(f"HTTP Server error: {e}")

if __name__ == '__main__':
    conf = config.Config()

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', help='Runs an HTTP server for the graphical interface', action='store_true')
    parser.add_argument('-p', '--port', help='Sets the port for the HTTP server (default: 8000)', default=8000)
    parser.add_argument('-o', '--offset', help='Number of days after the current date to search (default: 3)', default=3)
    parser.add_argument('-c', '--carriers', help='Manually select carriers (comma separated, e.g. "itabus,flixbus")')
    parser.add_argument('-io', '--interfaceonly', help='Only runs the interface, without searching', action='store_true')
    parser.add_argument('-ng', '--no-geocoding', help='Disable geocoding', action='store_true', default=False)

    args = parser.parse_args()

    Console.print_intro()
    
    # Validation
    try:
        args.port = int(args.port)
        args.offset = int(args.offset)
    except ValueError:
        Console.err('Invalid port or offset provided', True)

    # Configuration loading
    price_cap = conf.config.get('configuration', {}).get('price_cap', 20)
    delay = conf.config.get('configuration', {}).get('delay', 18000)
    geocoding_enabled = not args.no_geocoding

    # Carrier loading
    carriers = []
    ref = [c.strip() for c in args.carriers.split(',')] if args.carriers else Files.get_source_files('backend.discovery.carriers')
    
    for c in ref:
        try:
            carriers.append(__import__('backend.discovery.carriers.' + c, fromlist=[None]))
        except ImportError as e:
            Console.err(f'Could not import carrier \'{c}\': {e}')

    # HTTP Server
    if args.interface or args.interfaceonly:
        server_thread = threading.Thread(target=run_http_server, args=(args.port,), daemon=True)
        server_thread.start()
        Console.info(f'HTTP Server running on http://localhost:{args.port}')
    
    Console.empty_line()

    if not args.interfaceonly:
        orchestrator = DiscoveryOrchestrator(
            carriers=carriers,
            delay=delay,
            offset=args.offset,
            data_file=data_file,
            geocoding_enabled=geocoding_enabled
        )
        
        if args.interface:
            # Run in background if interface is also requested
            threading.Thread(target=orchestrator.run, daemon=True).start()
            # Keep main thread alive
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                Console.info("Shutting down...")
        else:
            # Run in foreground
            try:
                orchestrator.run()
            except KeyboardInterrupt:
                Console.info("Shutting down...")
    else:
        # Interface only: just keep the process alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            Console.info("Shutting down...")