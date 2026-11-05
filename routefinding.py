import csv
import pandas as pd
from datetime import date
from pathlib import Path

DATA_DIR = Path("GTFS_data")
filename_trips = DATA_DIR / "trips.txt"  # File name
file_name_schedule = DATA_DIR / "calendar_dates.txt"
fields = []  # Column names
rows = []  # Data rows

def get_current_date() -> str:
    return date.today().strftime("%Y%m%d")


def get_trips_for_date(date_str: str) -> pd.DataFrame:
    schedule = pd.read_csv(file_name_schedule)
    # exception_type 1 = service added on this date, 2 = service removed
    curr_calendar_dates = schedule[
        (schedule["date"] == int(date_str)) & (schedule["exception_type"] == 1)
    ]
    trips = pd.read_csv(filename_trips)
    curr_trips = trips[trips["service_id"].isin(curr_calendar_dates["service_id"])]
    return curr_trips

'''
What do we want?
We will know our date, destination, starting point, and an arrival time.
We want to return a list of paths. A path is defined as a 2d array, a list of legs. 
A leg is an array with four values: trip, start_stop, start_time, end_stop, and end_time.
Each leg should be able to map to two rows in stop_times.txt.
One row whose trip_id, arrival_time, and stop_id are the same as the leg's trip, start_time and start_stop values.
And another whose trip_id, arrival_time, and stop_id are the same as the leg's trip, end_time and end_stop values.
If there is more than 1 leg in the path, each leg's end time and end stop should be the same value as the next leg's start_time and start_stop values
'''

