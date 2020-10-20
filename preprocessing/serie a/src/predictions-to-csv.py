'''
    In this script I will reformat the prediction data from json to csv format
    Fields needed (ordered list):  
        - fixture_id
        - home_team_id
        - home_team_name
        - away_team_id
        - away_team_name
        - winning_percent_home
        - winning_percent_draws
        - winning_percent_away
        - forme_home
        - forme_away
        - att_home
        - att_away
        - def_home
        - def_away
        - fish_law_home
        - fish_law_away
        - h2h_home
        - h2h_away
        - goals_h2h_home
        - goals_h2h_away

'''

import json
import csv

fields = [
        "fixture_id",
        "home_team_id",
        "home_team_name",
        "away_team_id",
        "away_team_name",
        "winning_percent_home",
        "winning_percent_draws",
        "winning_percent_away",
        "forme_home",
        "forme_away",
        "att_home",
        "att_away",
        "def_home",
        "def_away",
        "fish_law_home",
        "fish_law_away",
        "h2h_home",
        "h2h_away",
        "goals_h2h_home",
        "goals_h2h_away"
]

with open("../data/pred_next10_fix_serieA.json", ) as predictions_file:
    predictions_json = json.load(predictions_file)
    #print(json.dumps(predictions_json, indent=4))

    predictions_list = []

    for pred in predictions_json:
        predictions_list.append(pred[0])

    rows = []
    rows.append(fields)

    for pred in predictions_list:
        row = []

        row.append(pred["fixture_id"])
        row.append(pred["teams"]["home"]["team_id"])
        row.append(pred["teams"]["home"]["team_name"])
        row.append(pred["teams"]["away"]["team_id"])
        row.append(pred["teams"]["away"]["team_name"])
        row.append(pred["winning_percent"]["home"])
        row.append(pred["winning_percent"]["draws"])
        row.append(pred["winning_percent"]["away"])
        row.append(pred["comparison"]["forme"]["home"])
        row.append(pred["comparison"]["forme"]["away"])
        row.append(pred["comparison"]["att"]["home"])
        row.append(pred["comparison"]["att"]["away"])
        row.append(pred["comparison"]["def"]["home"])
        row.append(pred["comparison"]["def"]["away"])
        row.append(pred["comparison"]["fish_law"]["home"])
        row.append(pred["comparison"]["fish_law"]["away"])
        row.append(pred["comparison"]["h2h"]["home"])
        row.append(pred["comparison"]["h2h"]["away"])
        row.append(pred["comparison"]["goals_h2h"]["home"])
        row.append(pred["comparison"]["goals_h2h"]["away"])

        rows.append(row)
    
        #print(row)

with open("../data/pred_next10_fix_serieA.csv", "w", newline='') as predictions_csv:
    writer = csv.writer(predictions_csv, delimiter=',')

    for row in rows:
        writer.writerow(row)
