"""
Module to interact with the database.
"""
import re
import sqlite3
from traceback import print_tb
from . import placeholders
from . import db_ops
import random
db_ops.ensure_db()
from sqlalchemy import create_engine, MetaData, Table,select
engine = create_engine("sqlite:///trains.db", echo=True)
meta = MetaData(bind=engine)
train_table = Table("train", meta, autoload=True)
station_table = Table("station", meta, autoload=True)
schedule_table = Table("schedule", meta, autoload=True)
booking_table = Table("booking", meta, autoload=True)

def exec_query(q, commit=False):
    conn = sqlite3.connect("trains.db")
    curs = conn.cursor()

    try:
        curs.execute(q)
        if commit:
            conn.commit()

        columns = [c[0] for c in curs.description]
        rows = curs.fetchall()
    finally:
        conn.close()

    return columns, rows
def search_stations(q):

    """Returns the top ten stations matching the given query string.

    This is used to get show the auto complete on the home page.

    The q is the few characters of the station name or
    code entered by the user.
    """
    col, rows = exec_query(f"select * from station where code = '{q.upper()}' or name like '%{q}%' ;")
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
    col, rows = exec_query(f"select * from train \
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
    col, rows = exec_query(f"select * from schedule \
         where train_number = '{int(train_number)}';")
    s = schedule_table
    sa = select([ s.c.station_code ,
                s.c.station_name ,
                s.c.train_number ,
                s.c.train_name ,
                s.c.day ,
                s.c.arrival ,
                s.c.departure ]).where(s.c.train_number == int(train_number))
    rows = (list(sa.execute()))
    # print((rows[0:10]))
    sch = []
    for row in rows:
        # print(row)
        d = {"station_code": row[0], "station_name":  row[1], "day": row[4], "arrival": row[5], "departure":row[6]}
        sch.append(d)
    
    return sch

def book_ticket(train_number, ticket_class, departure_date, 
                passenger_name, passenger_email):
    
    t = train_table
    sa = select([ t.c.from_station_code ,
                t.c.to_station_code ,
                t.c.from_station_name,
                t.c.to_station_name,
                t.c.name
                ]).where(t.c.number == int(train_number))
    station_codes = (list(sa.execute())[0])
   
    q = (f"insert into booking \
    ( train_number , passenger_name , passenger_email ,ticket_class ,date,from_station_code , to_station_code ) \
        values \
    ('{train_number}','{passenger_name}','{passenger_email}','{ticket_class}','{departure_date}','{station_codes[0]}','{station_codes[1]}')")
    conn = sqlite3.connect("trains.db")
    curs = conn.cursor()

    try:
        curs.execute(q)
        conn.commit()
        rows = curs.fetchall()    
    finally:
        conn.close()
    print("book ticket",rows)
    d = {
        "train_number":train_number,
        "train_name": station_codes[-1],
        "from_station_code": station_codes[0],
        "from_station_name":station_codes[2],
        "to_station_code": station_codes[1],
        "to_station_name": station_codes[3],
        "ticket_class": ticket_class,
        "date": departure_date,
        "passenger_name": passenger_name,
        "passenger_email": passenger_email,
    }
    return d
book_ticket("12628","3A","2022-12-01","Evalu Ator","evalu@ator.dev")
def get_train_name(train_number):
    query = f"SELECT name FROM train WHERE number = '{train_number}'"
    name = db_ops.exec_query(query)
    return name[1][0][0]
def get_station_name(code):
    query = f"SELECT name FROM station WHERE code = '{code}'"
    name = db_ops.exec_query(query)
    return name[1][0][0]

def get_from_to_station_names(from_station_code, to_station_code):
    return [get_station_name(from_station_code), get_station_name(to_station_code)]


def get_trips(email):
    """Returns the bookings made by the user
    """
    # TODO: make a db query and get the bookings
    # made by user with `email`
    query = f"SELECT * FROM booking WHERE passenger_email = '{email}'"
    b = booking_table
    sa = select([   b.c.id ,
                    b.c.train_number,
                    b.c.from_station_code ,
                    b.c.to_station_code ,
                    b.c.passenger_name ,
                    b.c.passenger_email ,
                    b.c.ticket_class ,
                    b.c.date 
                ]).where(b.c.passenger_email == email)
    bookings = (list(sa.execute()))
    trips = db_ops.exec_query(query)
    print(bookings, trips)
    res = []
    for booking in bookings:
        d = {
            "train_number": booking[1],
            "train_name": get_train_name(booking[1]),
            "from_station_code": booking[2],
            "from_station_name": get_from_to_station_names(booking[2], booking[3])[0],
            "to_station_code": booking[3],
            "to_station_name": get_from_to_station_names(booking[2], booking[3])[1],
            "ticket_class": booking[6],
            "date": booking[7],
            "passenger_name": booking[4],
            "passenger_email": booking[5],
        }
        res.append(d)
    return res
print(get_trips("evaluator@example.com"))