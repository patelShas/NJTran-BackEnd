import zipfile
import requests
import os
from datetime import date
from njtran_backend.refreshData import getCurrentToken, updateToken
from njtran_backend.paths import GTFS_DATA_DIR, GTFS_ARCHIVE_DIR


# This returns Rail GTFS schedule data in ZIP format.


def getGTFS(save_path):
    # Check if file already exists
    if os.path.exists(save_path):
        raise FileExistsError(f"{save_path} already exists")

    # get token for requesting GTFS data
    updateToken()
    token = getCurrentToken()
    
    url = "https://testraildata.njtransit.com/api/GTFSRT/getGTFS"
    headers = {"accept": "*/*"}
    files = {"token": (None, token)}
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save the ZIP file
        with open(save_path, "wb") as f:
            f.write(response.content)
        print("GTFS data downloaded successfully")
    else:
        print(f"Error: {response.status_code}")
        
def data_refresh():
    # get new GTFS data first, so a failed download doesn't leave GTFS_data empty
    today = str(date.today())
    gtfs_zip_path = GTFS_ARCHIVE_DIR / f"gtfs_data_{today}.zip"
    # check if GTFS data for today's date already exists in GTFS_data_archive
    if os.path.exists(gtfs_zip_path):
        print("GTFS data for today's date already exists in GTFS_data_archive")
    else:
        getGTFS(save_path=gtfs_zip_path)
    if not os.path.exists(gtfs_zip_path):
        raise RuntimeError("GTFS download failed; keeping existing GTFS_data")

    # delete old GTFS data from folder GTFS_data
    if GTFS_DATA_DIR.exists():
        for file in GTFS_DATA_DIR.iterdir():
            file.unlink()

    # unzip the GTFS data and save it in the GTFS_data folder
    with zipfile.ZipFile(gtfs_zip_path, "r") as zip_ref:
        zip_ref.extractall(GTFS_DATA_DIR)
        
data_refresh()