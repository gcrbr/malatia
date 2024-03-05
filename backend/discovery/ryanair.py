from backend.discovery import tripobj
import dateutil.parser
import datetime
import requests

departure = 'NAP'

def get_date(offset=0):
    return (datetime.datetime.now() + datetime.timedelta(offset+1)).strftime('%Y-%m-%d')

def search_trips(offset=0):
    global departure
    trips = []
    try:
        search = requests.get('https://www.ryanair.com/api/farfnd/v4/oneWayFares',
        params={
            'departureAirportIataCode': departure,
            'outboundDepartureDateFrom': get_date(offset),
            'market': 'en-US',
            'adultPaxCount': '1',
            'outboundDepartureDateTo': get_date(offset),
            'outboundDepartureTimeFrom': '00:00',
            'outboundDepartureTimeTo': '23:59'
        }).json()
        for k in search['fares']:
            flight = k['outbound']
            if (price := flight['price']['value']) <= tripobj.good_price and price > 0:
                trips.append(
                    tripobj.Trip(
                        date=dateutil.parser.parse(flight['departureDate']),
                        departure='Napoli',
                        arrival=flight['arrivalAirport']['city']['name'],
                        carrier='Ryanair',
                        duration=(dateutil.parser.parse(flight['arrivalDate'])-dateutil.parser.parse(flight['departureDate'])).seconds/60,
                        price=price,
                        arrival_country=flight['arrivalAirport']['countryName']
                    ).to_dict()
                )
    except: pass
    return trips