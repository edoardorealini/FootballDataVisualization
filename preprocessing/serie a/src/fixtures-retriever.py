import requests
import json
import os

data_path = "../data/"
base_url = "https://api-football-v1.p.rapidapi.com/v2"
headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "8e365a2420msh9e37db3a35f23eep1b14fdjsn9ee9e26c21b6"
    }

fixtures_serieA = "/fixtures/league/2857" #cerca le fixtures della serie A 2020 codice lega 2857

url = base_url + fixtures_serieA

response = requests.request("GET", url, headers=headers)

fixtures_file = open(data_path + "serieA_fixtures", "w")
fixtures_file.write(str(response.json()))
