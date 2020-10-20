import requests
import pyjq

url = "https://api-football-v1.p.rapidapi.com/v2/players/squad/489/2020"

milan_player_stats = "https://api-football-v1.p.rapidapi.com/v2/players/team/489/2019-2020" 

fixtures = "https://api-football-v1.p.rapidapi.com/v2/fixtures/team/489/next/5"

milan_crotone = "https://api-football-v1.p.rapidapi.com/v2/predictions/608492"

milan_inter = "https://api-football-v1.p.rapidapi.com/v2/predictions/608512"

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "8e365a2420msh9e37db3a35f23eep1b14fdjsn9ee9e26c21b6"
    }

response = requests.request("GET", milan_inter, headers=headers)

print(response.text)

#file = open("leagues", "w")

#file.write(response.text)