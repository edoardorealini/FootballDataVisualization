import requests
import pyjq

data_path = "../data/"
base_url = "https://api-football-v1.p.rapidapi.com/v2"

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "8e365a2420msh9e37db3a35f23eep1b14fdjsn9ee9e26c21b6"
    }

leagues = "/leagues"
current_leagues = "/leagues/current"

url = base_url + current_leagues

response = requests.request("GET", url, headers=headers)

leagues_file = open(data_path + "current_leagues", 'w')

leagues_file.write(response.text)