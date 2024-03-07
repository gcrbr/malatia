from backend.discovery import multidiscovery
from backend.discovery import trip
import datetime

class Main(multidiscovery.Multidiscovery):
    def __init__(self):
        if 'Accept' in self.session.headers:
            del self.session.headers['Accept']
        self.session.headers['Content-Type'] = 'application/json'
        format = ('name', 'country', 'identifiers.italo')
        super().__init__(
            self.config.format_city_object(self.config.get_departure_city(), format),
            self.config.get_formatted_cities(format)
        )
    
    def get_ntv_signature(self):
        return self.session.post(
            'https://big.ntvspa.it/BIG/v7/Rest/SessionManager.svc/Login',
            json={
                'Login': {
                    'Domain': 'WWW',
                    'VersionNumber': '4.2.2',
                    'Password': 'F3hoM!n0$!ZE',
                    'Username': 'WWW_Anonymous'
                },
                'SourceSystem': 3
            },
        ).json().get('Signature')
    
    def get_dates(self, offset=0):
        format = '/Date(%d+0000)/'
        date = datetime.datetime.now() + datetime.timedelta(offset+1)
        d_date = datetime.datetime(
            day=date.day, 
            month=date.month, 
            year=date.year,
            hour=0,
        )
        a_date = datetime.datetime(
            day=date.day, 
            month=date.month, 
            year=date.year,
            hour=23,
            minute=59
        )
        d_time = int(d_date.timestamp()*1000)
        a_time = int(a_date.timestamp()*1000)
        return (format % d_time, format % a_time)
    
    def parse_date(self, obj):
        return datetime.datetime.fromtimestamp(int(obj[6:][:-10]))

    def search_location(self, p, offset):
        try:
            dates = self.get_dates(offset)
            search = self.session.post(
                'https://big.ntvspa.it/BIG/v7/Rest/BookingManager.svc/GetAvailableTrains',
                json={
                    'SourceSystem': 3,
                    'GetAvailableTrains': {
                        'RoundTrip': False,
                        'IDPartner': None,
                        'JourneySpecialOperation': None,
                        'InfantNumber': 0,
                        'IntervalStartDateTime': dates[0],
                        'DepartureStation': self.departure[2],
                        'ArrivalStation': p[2],
                        'IsGuest': True,
                        'AvailabilityFilter': 1,
                        'AncillaryService': None,
                        'Promocode': None,
                        'OverrideIntervalTimeRestriction': True,
                        'ProductClass': None,
                        'FareType': None,
                        'SeniorNumber': 0,
                        'IntervalEndDateTime': dates[1],
                        'InfoBoat': None,
                        'ShowNestedSSR': True,
                        'RoundtripProductClass': None,
                        'FareClassOfService': None,
                        'YoungNumber': 0,
                        'ProductName': None,
                        'ShowFareBasisRestrictionRules': True,
                        'FareClassControl': 0,
                        'CurrencyCode': 'EUR',
                        'RoundTripIntervalEndDateTime': dates[0],
                        'RoundTripIntervalStartDateTime': dates[1],
                        'AdultNumber': 1,
                        'AgentPromotion': None,
                        'ChildNumber': 0
                    },
                    'Signature': self.get_ntv_signature()
                },
                headers={
                    'Content-Type': 'application/json'
                }
            ).json()

            for train in search['JourneyDateMarkets'][0]['Journeys']:
                train = train['Segments'][0]
                if (price := train['Fares'][0]['FullFarePrice']) <= trip.good_price and price > 0:
                    self.trips.append(
                        trip.Trip(
                            date=(dpt:=self.parse_date(train['STD'])),
                            departure=self.departure[0],
                            arrival=p[0],
                            carrier=self.base_name(__name__),
                            duration=(self.parse_date(train['STA'])-dpt).seconds/60,
                            price=price,
                            arrival_country='Italy'
                        ).to_dict()
                    )
        except:
            pass
            