import threading
import colorama
import argparse
import utils
import glob
import json
import os
import math
from backend.populate import model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--departure', help='Enter the departure city for which to search the destinations (es. "-d naples")')
    parser.add_argument('-c', '--carriers', help='Manually select the carriers to research on, separated by a comma (es. "-c itabus,flixbus", default: all)')

    args = parser.parse_args()

    utils.print_intro()
    print(f'{colorama.Fore.YELLOW}This feature is still in the testing phase{colorama.Style.RESET_ALL}\n')

    if not args.departure:
        utils.err('Missing departure city', True)
    
    carriers = list()
    full_reach = list()
    threads = list()
    for c in utils.get_source_files('backend.populate.carriers'):
        if args.carriers and not c in args.carriers.lower().split(','):
            continue

        carrier = __import__('backend.populate.carriers.' + c, fromlist=[None])
        carrier_name = c.split('.')[-1]

        print(f'{colorama.Fore.GREEN}(!) Searching destinations for \'{carrier_name}\'')

        def add_place(carrier_name, place):
            global full_reach
            print(f'{colorama.Fore.CYAN}(>) Found destination \'{place.name}\' on \'{carrier_name}\'{colorama.Style.RESET_ALL}')
            place.carrier = carrier_name
            full_reach.append(place)

        def normalize(carrier_obj, carrier_name, reach):
            for place in reach:
                try:
                    place = carrier_obj.normalize(place)
                except:
                    utils.err(f'Unable to normalize \'{place.name}\'')
                if not place:
                    continue
                add_place(carrier_name, place)

        def _(carrier, carrier_name):
            carrier_obj = carrier.Main()
            reach = carrier_obj.get_reach(args.departure)
            
            if carrier_obj.normalization:
                ratio = 0.15
                amt_threads = round(len(reach) * ratio)
                reach_division = list()
                for i in range(amt_threads):
                    reach_division.append(list())
                for i in range(len(reach)):
                    reach_division[math.ceil(i * ratio) - 1].append(reach[i])

                sub_threads = list()
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

    file = open('config.json', 'w+')
    fallback = json.dumps({
            'configuration': {
                'departure': args.departure,
                'price_cap': 20,
                'delay': 18000
            },
            'cities': full_reach,
        }, indent=4, cls=model.RouteEncoder)

    if not os.path.isfile('config.json'):
        file.write(fallback)
        file.close()
    else:
        try:
            data = file.read()
            current = json.loads(data)
            current['cities'] += full_reach
            file.write(json.dumps(current, indent=4))
            file.close()
        except:
            utils.err('Invalid JSON data in config.json')
            file.write(fallback)
            file.close()

    print(f'\n{colorama.Fore.YELLOW}(!) {len(full_reach)} destinations saved on config.json{colorama.Style.RESET_ALL}')