import requests
import json

base_url = "https://api-football-v1.p.rapidapi.com/v2"

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "8e365a2420msh9e37db3a35f23eep1b14fdjsn9ee9e26c21b6"
    }

url = base_url + "/statistics/fixture/608481"

response = requests.request("GET", url, headers=headers)

json_data = response.json()

print(json.dumps(json_data, indent=4))
