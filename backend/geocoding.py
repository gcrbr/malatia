import requests

coord_cache = {}
country_cache = {}

def api_call(query):
    return requests.get('https://www.waze.com/live-map/api/autocomplete',
        params={
            'q': query,
            'exp': '0,0,0',
            'geo-env': 'row',
            'v': '0,0;0,0',
            'lang': 'it'
        },
        headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/100.0.1185.39'
        }
    ).json()

def get_coordinates(city):
    global coord_cache
    city = city.lower()
    if not city in coord_cache:
        lat, lon = 0, 0
        try:
            waze = api_call(city)
            c = waze[0]
            lat, lon = c['latLng']['lat'], c['latLng']['lng']
        except:
            pass
        coord_cache[city] = (float(lat), float(lon))
    return coord_cache[city]

def get_country(city):
    global country_cache
    city = city.lower()
    if not city in country_cache:
        country = ''
        try:
            waze = api_call(city)
            c = waze[0]
            country = c['address'].split(', ')[-1]
        except:
            pass
        country_cache[city] = country
    return country_cache[city]