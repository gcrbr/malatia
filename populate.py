import threading
import colorama
import argparse
import utils
import glob
import json
import os

def err(text, _exit=False):
    print(f'\n{colorama.Fore.RED}(!) {text}{colorama.Style.RESET_ALL}')
    if _exit:
        exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--city', help='Enter the departure city for which to search the destinations (es. "-c naples")')

    args = parser.parse_args()

    utils.print_intro()
    print(f'{colorama.Fore.YELLOW}This feature is still in the testing phase{colorama.Style.RESET_ALL}\n')

    if not args.city:
        utils.err('Missing departure city', True)
    
    ref = [os.path.basename(f)[:-3] for f in glob.glob('backend/populate/carriers/*.py')]
    carriers = []
    full_reach = []
    threads = []
    for c in ref:
        carrier = __import__('backend.populate.carriers.' + c, fromlist=[None])
        carrier_name = c.split('.')[-1]
        print(f'{colorama.Fore.GREEN}(!) Searching destinations for \'{carrier_name}\'')

        def _(carrier, carrier_name):
            global full_reach
            reach = carrier.Main().get_reach(args.city)
            for place in reach:
                if carrier.NORMALIZE:
                    place = carrier.Main().normalize(place[3][0], place[3][1])
                    if not place:
                        continue
                print(f'{colorama.Fore.CYAN}(>) Found destination \'{place[0]}\' on \'{carrier_name}\'{colorama.Style.RESET_ALL}')
                full_reach.append({
                    'name': place[0],
                    'country': place[1],
                    'identifiers': {
                        carrier_name: place[2]
                    }
                })
        
        threads.append((t := threading.Thread(target=_, args=(carrier, carrier_name,))))
        t.start()
    
    for t in threads:
        t.join()

    file = open('config.json', 'r+')

    if not os.path.isfile('config.json') or not (data := file.read()):
        file.write(json.dumps({
            'configuration': {
                'departure': args.city,
                'price_cap': 20,
                'delay': 18000
            },
            'cities': full_reach,
        }, indent=4))
        file.close()
    else:
        try:
            current = json.loads(data)
        except:
            utils.err('Invalid JSON data in config.json')
        current['cities'] += full_reach
        file.write(json.dumps(current), indent=4)
        file.close()

    print(f'\n{colorama.Fore.YELLOW}(!) {len(full_reach)} destinations saved on config.json{colorama.Style.RESET_ALL}')