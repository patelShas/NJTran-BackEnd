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

