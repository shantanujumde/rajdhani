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
    res = db_ops.exec_query(f"select * from train where from_station_code like '%{q}%';")
    # TODO: make a db query to get the matching stations
    # and replace the following dummy implementation
    # print(res[0])
    # ans = []
    # for val in res[-1]:
    #     print(val)
    #     d = {"code":val[0], "name":val[1]}
    #     ans.append(d)
    ans = []
    return ans
# {"code": "ADI", "name": "AHMEDABAD JN"},
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
    # TODO: make a db query to get the matching trains
    # and replace the following dummy implementation
    col, rows = db_ops.exec_query(f"select * from train where from_station_code like '%{from_station_code}%' and to_station_code like '%{to_station_code}%'  ;")
    # print(col)
    ans = []
    for val in rows:
        # print(val)
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
        ans.append(d)
    return ans
print(search_trains('SBC', 'MAS'))
def get_schedule(train_number):
    """Returns the schedule of a train.
    """
    return placeholders.SCHEDULE

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
