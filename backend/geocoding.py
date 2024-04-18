import requests
import random
import time

cache = {}

def random_number(l):
    r = ''
    for x in range(l):
        r += str(random.randint(0, 9))

def generate_reqid():
    return f'{int(time.time()*3)}_{random_number(6)}'

def generate_spn():
    return f'{random.uniform(0,0.1)},{random.uniform(0,0.1)}'

def generate_yu():
    return random_number(19)

def get_coordinates(city):
    global cache
    city = city.lower()
    if not city in cache:
        lat, lon = 0, 0
        try:
            yandex = requests.get('https://suggest-maps.yandex.com/suggest-geo',
            params={
                'add_chains_loc': '1',
                'add_coords': '1',
                'add_rubrics_loc': '1',
                'bases': 'geo,biz,transit',
                'client_reqid': generate_reqid(),
                'fullpath': '1',
                'lang': 'it',
                'll': '45.768,10.723',
                'origin': 'maps-search-form',
                'outformat': 'json',
                'part': city,
                'pos': '9',
                'spn': generate_spn(),
                'v': '9',
                'yu': generate_yu()
            },
            headers={
                'origin': 'https://yandex.com',
                'referer': 'https://yandex.com/maps/',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/100.0.1185.39'
            }).json()
            
            c = yandex['results'][0]

            '''for result in yandex['results']:
                if 'locality' in result['tags']:
                    c = result
                    break'''
            
            lat, lon = c['pos'].split(',')[::-1]
            cache[city] = (float(lat), float(lon))
        except Exception as e:
            print(e)
    return cache[city]