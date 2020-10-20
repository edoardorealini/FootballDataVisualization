import json

input_file = open("../data/leagues.json", )
out_file = open("../data/2020_leagues", "w")

json_data = json.load(input_file)

for league in json_data["api"]["leagues"]:
    if league["season"] == 2020:
        out_file.write(json.dumps(league))
        #print(json.dumps(league))

