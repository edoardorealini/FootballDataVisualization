import requests
import json
from retriever_library import *
import time
#import pandas as pd

data_path = "../data/"
base_url = "https://api-football-v1.p.rapidapi.com/v2"

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "8e365a2420msh9e37db3a35f23eep1b14fdjsn9ee9e26c21b6"
    }

serie_a_leagueid = 2857
juventus_teamid = 496
milan_teamid = 489

#get_teams_from_league("serieA_teams.json", serie_a_leagueid)
#get_team_statistics_date("juventus_stats_until_2019-05-27.json", juventus_teamid, serie_a_leagueid, "2020-05-27")
#get_team_statistics("milan_until_today.json", team_id=milan_teamid, league_id=serie_a_leagueid)
#get_seasonAvailable_by_league("serieA_seasons.json", serie_a_leagueid)

leagues_full = ["713", "712", "711", "710", "709", "708", "66", "28", "94", "891", "2857"]
leagues_last = ["2857"]
season = 2020

for league in leagues_last:
    print("Retrieving data for league ", league, " and season ", season)
    get_oldTeams_statistics([league], season)
    season = season + 1
    print("Waiting 70 seconds")
    time.sleep(70)