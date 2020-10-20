import requests
import json
from retriever_library import *
import time
#import pandas as pd

data_path = "../data/serieA-fixtures/"
base_url = "https://api-football-v1.p.rapidapi.com/v2"

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "8e365a2420msh9e37db3a35f23eep1b14fdjsn9ee9e26c21b6"
    }


leagues_full = ["713", "712", "711", "710", "709", "708", "66", "28", "94", "891", "2857"]
season = 2010

for league in leagues_full:
    print("Retrieving data for league ", league, " of season ", season)
    get_fixtures_by_league("serieA-fixtures/all-fixtures-" + str(season) + ".json", league)
    season = season + 1
    print("Waiting 1 second")
    time.sleep(1)