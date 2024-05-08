import requests

cache = {}

def get_coordinates(city):
    global cache
    city = city.lower()
    if not city in cache:
        lat, lon = 0, 0
        try:
            waze = requests.get('https://www.waze.com/live-map/api/autocomplete',
            params={
                'q': city,
                'exp': '0,0,0',
                'geo-env': 'row',
                'v': '0,0;0,0',
                'lang': 'it'
            },
            headers={
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36 Edg/100.0.1185.39'
            }).json()
            
            c = waze[0]
            
            lat, lon = c['latLng']['lat'], c['latLng']['lng']
        except:
            pass
        cache[city] = (float(lat), float(lon))
    return cache[city]