import csv
import pandas as pd
from datetime import date

filename_trips = ".\getGTFS\\trips.csv"  # File name
file_name_schedule = ".\getGTFS\\calendar_dates.csv"
fields = []  # Column names
rows = []  # Data rows

def get_current_date() -> str:
    today = date.today()
    curr_year = str(today.year)
    curr_month = str(today.month)
    if len(curr_month) < 2:
        curr_month = "0" + curr_month
    curr_day = str(today.day)
    curr_date = curr_year + curr_month + curr_day
    return curr_date

print(get_current_date())

exit()
schedule = pd.read_csv(file_name_schedule)
curr_services = schedule[schedule["date"] == int(curr_date)]

trips = pd.read_csv(filename_trips)
print(f"there are {len(trips)} trips")
main_line_trips = trips[trips["route_id"] == 6]
print(f"{len(main_line_trips)} of those are on the main line")
