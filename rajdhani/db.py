"""
Module to interact with the database.
"""

from . import placeholders
from . import db_ops

db_ops.ensure_db()


def search_stations(q):

    """Returns the top ten stations matching the given query string.

    This is used to get show the auto complete on the home page.

    The q is the few characters of the station name or
    code entered by the user.
    """
    col, rows = db_ops.exec_query(f"select * from station where code = '{q.upper()}' or name like '%{q}%' ;")
    # TODO: make a db query to get the matching stations
    # and replace the following dummy implementation
    ans = []
    for val in rows:
        # print(val)
        d = {"code":val[0], "name":val[1]}
        ans.append(d)
        # print(val[4],val) 
    return ans
# {"code": "ADI", "name": "AHMEDABAD JN"},
from datetime import datetime

def search_trains(
        from_station_code,
        to_station_code,
        ticket_class=None,
        departure_date=None,
        departure_time=[],
        arrival_time=[]):
    """Returns all the trains that source to destination stations on
    the given date. When ticket_class is provided, this should return
    only the trains that have that ticket class.

    This is used to get show the trains on the search results page.
    """
    slot1 = datetime.strptime('00:00:00', '%H:%M:%S')
    slot2 = datetime.strptime('08:00:00', '%H:%M:%S')
    slot3 = datetime.strptime('12:00:00', '%H:%M:%S')
    slot4 = datetime.strptime('16:00:00', '%H:%M:%S')
    slot5 = datetime.strptime('20:00:00', '%H:%M:%S')

    # TODO: make a db query to get the matching trains
    # and replace the following dummy implementation
    col, rows = db_ops.exec_query(f"select * from train \
        where from_station_code like \
        '%{from_station_code}%' and \
        to_station_code like '%{to_station_code}%'\
                ;")
    filter1 = []
    for val in rows:
        d = {
            "number": val[0],
            "name": val[1],
            "from_station_code":val[4],
            "from_station_name": val[5],
            "to_station_code": val[6],
            "to_station_name": val[7],
            "departure": val[8],
            "arrival": val[9],
            "duration_h": val[10],
            "duration_m": val[11]
        }
        if ticket_class == "SL" and val[-6] == 1:
            filter1.append(d)
        elif ticket_class == "CC" and val[-1] == 1:
            filter1.append(d)
        elif ticket_class == "1A" and val[-3] == 1:
            filter1.append(d)
        elif ticket_class == None:
            filter1.append(d)
    
    if departure_time or arrival_time:
        filter2 = []
        for val in filter1:
            for slot in departure_time:
                if slot == "slot1" and slot1 <= datetime.strptime(val["departure"], '%H:%M:%S') and slot2>= datetime.strptime(val["departure"], '%H:%M:%S'):
                        filter2.append(val)
                if slot == "slot2" and slot2 <= datetime.strptime(val["departure"], '%H:%M:%S') and slot3>= datetime.strptime(val["departure"], '%H:%M:%S'):
                        filter2.append(val)
                if slot == "slot3" and slot3 <= datetime.strptime(val["departure"], '%H:%M:%S') and slot4>= datetime.strptime(val["departure"], '%H:%M:%S'):
                        filter2.append(val)
                if slot == "slot4" and slot4 <= datetime.strptime(val["departure"], '%H:%M:%S') and slot5>= datetime.strptime(val["departure"], '%H:%M:%S'):
                        filter2.append(val)
                if slot == "slot5" and slot5 < datetime.strptime(val["departure"], '%H:%M:%S'):# and slot1<= datetime.strptime(val["departure"], '%H:%M:%S'):
                        filter2.append(val)
            for slot in arrival_time:
                if slot == "slot1" and slot1 <= datetime.strptime(val["arrival"], '%H:%M:%S') and slot2>= datetime.strptime(val["arrival"], '%H:%M:%S'):
                        filter2.append(val)
                if slot == "slot2" and slot2 <= datetime.strptime(val["arrival"], '%H:%M:%S') and slot3>= datetime.strptime(val["arrival"], '%H:%M:%S'):
                        filter2.append(val)
                if slot == "slot3" and slot3 <= datetime.strptime(val["arrival"], '%H:%M:%S') and slot4>= datetime.strptime(val["arrival"], '%H:%M:%S'):
                        filter2.append(val)
                if slot == "slot4" and slot4 <= datetime.strptime(val["arrival"], '%H:%M:%S') and slot5>= datetime.strptime(val["arrival"], '%H:%M:%S'):
                        filter2.append(val)
                if slot == "slot5" and slot5 < datetime.strptime(val["arrival"], '%H:%M:%S'):# and slot1<= datetime.strptime(val["arrival"], '%H:%M:%S'):
                        filter2.append(val)
        return filter2
    return filter1
# for i in (search_trains('BCT', 'ADI',arrival_time=["slot1"], ticket_class="1A")):
#     print(i["number"])
def get_schedule(train_number):
    """Returns the schedule of a train.
    {"station_code": "BCT", "station_name": "Mumbai Central", "day": "1.0", "arrival": "None", "departure": "23:25:00"},ß
    =>['number', 'name', 'type', 'zone', 'from_station_code', 'from_station_name', 'to_station_code', 'to_station_name', 'departure', 
    'arrival', 'duration_h', 'duration_m', 'distance', 'return_train', 'sleeper', 'third_ac', 'second_ac', 'first_ac', 'first_class', 
    'chair_car'] 
    =>['code', 'name', 'zone', 'state', 'address', 'latitude', 'longitude']
    """
    col, rows = db_ops.exec_query(f"select * from train \
         where number = '{int(train_number)}';")
    print(len(rows))
    row = rows[0]
    sch = [
        row[4],
        row[5],
        '1' if 1 in row[14:] else '0',
        str("-"),
        row[8][:5]
    ]
    
    return sch
print(get_schedule("12028"))

def book_ticket(train_number, ticket_class, departure_date, passenger_name, passenger_email):
    """Book a ticket for passenger
    """
    # TODO: make a db query and insert a new booking
    # into the booking table

    return placeholders.TRIPS[0]

def get_trips(email):
    """Returns the bookings made by the user
    """
    # TODO: make a db query and get the bookings
    # made by user with `email`

    return placeholders.TRIPS
