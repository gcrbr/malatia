from backend.discovery import tripobj
import dateutil.parser
import threading
import requests
import datetime

departure = ('Napoli', 'NAP_T')
arrivals = [
    ('Milano', 'MIL_T'),
    ('Torino', 'TOR_T'),
    ('Roma', 'ROM_T'),
    ('Palermo', 'PAM_T'),
    ('Agrigento', 'AGR_T'),
    ('Aosta', 'AOT_T'),
    ('San Benedetto del Tronto', 'SBN_T'),
    ('L\'Aquila', 'LAQ_T'),
    ('Catania', 'CAT_T'),
    ('Firenze', 'FIR_T'),
    ('Venezia', 'VEN_T'),
    ('Bologna', 'BOL_T'),
    ('Bergamo', 'BGG_T'),
    ('Mantova', 'MAN_T'),
    ('Verona', 'VER_T'),
    ('Reggio Emilia', 'REG_T'),
    ('Bari', 'BAR_T')
]
trips = []

def get_date(offset=0):
    return (datetime.datetime.now() + datetime.timedelta(offset+1)).strftime('%Y-%m-%d')

def search_location(p, offset):
    global trips, departure
    try:
        search = requests.get(f'https://www.itabus.it/on/demandware.store/Sites-ITABUS-Site/it/Api-Travels?origin={departure[1]}&destination={p[1]}&datestart={get_date(offset)}&adults=1&children=0&membership=false').json()
        for trip in search['data']['outbound']['routes']:
            if (price := trip['bundles']['BASIC'][0]['price']) < tripobj.good_price and price > 0:
                trips.append(
                    tripobj.Trip(
                        date=dateutil.parser.isoparse(trip['departure_timestamp']),
                        departure=departure[0],
                        arrival=p[0],
                        carrier='Itabus',
                        duration=(dateutil.parser.isoparse(trip['arrival_timestamp']) - dateutil.parser.isoparse(trip['departure_timestamp'])).seconds/60,
                        price=price,
                        arrival_country='Italy'
                    ).to_dict()
                )
    except:
        pass

def search_trips(offset=0):
    global arrivals
    threads = []
    for p in arrivals:
        thread = threading.Thread(target=search_location, args=(p, offset,))
        threads.append(thread)
        thread.start()
    for t in threads:
        t.join()
    return trips