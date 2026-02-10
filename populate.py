import threading
import argparse
import json
import os
from backend.populate import model
from utils import Console, Files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--departure', help='Enter the departure city for which to search the destinations (es. "-d naples")')
    parser.add_argument('-c', '--carriers', help='Manually select the carriers to research on, separated by a comma (es. "-c itabus,flixbus", default: all)')

    args = parser.parse_args()
    chosen_carriers = args.carriers.lower().split(',') if args.carriers else []

    Console.print_intro()
    Console.warning('This feature is still in the testing phase')

    if not args.departure:
        Console.err('Missing departure city', True)
    
    carriers = []
    full_reach = []
    threads = []
    for c in Files.get_source_files('backend.populate.carriers'):
        if args.carriers and not c in chosen_carriers:
            continue

        carrier = __import__('backend.populate.carriers.' + c, fromlist=[None])
        carrier_name = c.split('.')[-1]

        Console.info(f'Searching destinations for \'{carrier_name}\'')

        def add_place(carrier_name, place):
            global full_reach
            Console.info(f'Found destination \'{place.name}\' on \'{carrier_name}\'')
            place.carrier = carrier_name
            full_reach.append(place)

        def normalize(carrier_obj, carrier_name, reach):
            for place in reach:
                try:
                    place = carrier_obj.normalize(place)
                except Exception as e:
                    Console.err(f'Unable to normalize \'{place.name}\': {e}')
                if not place:
                    continue
                add_place(carrier_name, place)

        def _(carrier, carrier_name):
            carrier_obj = carrier.Main()
            reach = carrier_obj.get_reach(args.departure)
            
            if carrier_obj.normalization:
                ratio = 0.15
                amt_threads = max(1, round(len(reach) * ratio))
                reach_division = [[] for _ in range(amt_threads)]
                for i, place in enumerate(reach):
                    reach_division[i % amt_threads].append(place)

                sub_threads = []
                for content in reach_division:
                    sub_threads.append((t := threading.Thread(target=normalize, args=(carrier_obj, carrier_name, content,))))
                    t.start()
                for t in sub_threads:
                    t.join()
            else:
                for place in reach:
                    add_place(carrier_name, place)

        threads.append((t := threading.Thread(target=_, args=(carrier, carrier_name,))))
        t.start()
    
    for t in threads:
        t.join()

    config_path = 'config.json'
    config_data = {
        'configuration': {
            'departure': args.departure,
            'price_cap': 20,
            'delay': 18000
        },
        'cities': []
    }

    if os.path.isfile(config_path):
        try:
            with open(config_path, 'r') as f:
                config_data = json.load(f)
        except Exception as e:
            Console.err(f'Failed to read {config_path}: {e}. Initializing new config.')

    if 'cities' not in config_data:
        config_data['cities'] = []

    config_data['cities'] += full_reach

    # grouping
    grouped_cities = {}
    for city in config_data['cities']:
        if isinstance(city, model.Route):
            name = city.name
            country = city.country
            new_ids = {city.carrier: city.id}
        else:
            name = city.get('name')
            country = city.get('country')
            new_ids = city.get('identifiers', {})

        if not name:
            continue

        lookup_name = name.lower()
        if lookup_name not in grouped_cities:
            grouped_cities[lookup_name] = {
                'name': name,
                'country': country,
                'identifiers': {}
            }
        
        grouped_cities[lookup_name]['identifiers'].update(new_ids)
        if country and not grouped_cities[lookup_name]['country']:
            grouped_cities[lookup_name]['country'] = country
    
    config_data['cities'] = list(grouped_cities.values())

    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=4, cls=model.RouteEncoder)

    Console.empty_line()
    Console.info(f'{len(full_reach)} destinations saved on config.json')