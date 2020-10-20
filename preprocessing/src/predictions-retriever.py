import requests
import json
import os

data_path = "../data/"
base_url = "https://api-football-v1.p.rapidapi.com/v2"
headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "8e365a2420msh9e37db3a35f23eep1b14fdjsn9ee9e26c21b6"
    }


predictions_path = "/predictions/"
league_code = 2857 #league code for Serie A Italia 2020 

fixtures_filepath = data_path + "next10_serieA_fixtures.json"
fixtures_file = open(fixtures_filepath, )
fixtures_json = json.load(fixtures_file)

predictions = []

for fixture in fixtures_json:
    fixture_code = fixture["fixture_id"]
    print(fixture_code)
    url = base_url + predictions_path + str(fixture_code)
    response = requests.request("GET", url, headers=headers)
    predictions.append(response.json()["api"]["predictions"])

predictions_file = open(data_path + "predictions_serieA_next10", 'w')
predictions_file.write(str(predictions))

predictions_file.close()