import requests
import json
from retriever_library import fixtures_stats_csv_generator
import time
import pandas as pd
import numpy as np

in_file_path = "serieA-fixtures/all-fixtures-"

for season in range(2010,2020):
    fixtures_stats_csv_generator(input_file_json=in_file_path + str(season) + ".json", 
                                out_file_csv_path="../data/" + in_file_path + str(season) + ".csv")


'''
Now we want to generate a file for each season with the following structure:
each row represents a team for the season
in each row there must be the following elements:
    - team id
    - team name
    - one column for each round with the points that the team has earned so far.
'''

#using pandas

for season in range(2010, 2020):

    data = pd.read_csv("../data/serieA-fixtures/all-fixtures-" + str(season) + ".csv")

    winners = []
    rounds = []    

    #while reading each row of the dataframe i want to add a column containing the result of the match as follow
    #the name of the team that has won, otherwise the word "draw"

    for index, row in data.iterrows():
        if row["goals_home_team"] > row["goals_away_team"]:
            winners.append(row["home_team_name"])
        
        if row["goals_home_team"] < row["goals_away_team"]:
            winners.append(row["away_team_name"])

        if row["goals_home_team"] == row["goals_away_team"]:
            winners.append("draw")

        rounds.append(row["round"].replace("Regular Season - ", ""))
            
    if(len(winners) != 380):
        for index in range(len(winners) - 1, 379):
            winners.append("TBD")

    np_winners = np.array(winners)
    data["winner"] = np_winners
    data["round"] = rounds

    data.to_csv("../data/" + in_file_path + str(season) + ".csv")


cols = []
for index in range(0, 38):
    cols.append("round_" + str(index + 1))


#now we have to: for each season generate a new csv file containing the points, updated per each round for every team of such season
for season in range(2010, 2020):
    print("Processing season " + str(season))

    data = pd.read_csv("../data/serieA-fixtures/all-fixtures-" + str(season) + ".csv")

    data = data.sort_values(by='round', ascending=True)

    teams = data["home_team_name"]
    
    #getting the list of the unique teams names
    teams_set = set(teams)
    teams = list(teams_set)

    points = {}
    for team in teams:
        points[team] = []
        for i in range(0, 38):
            points[team].append(0)

    for index, row in data.iterrows():

        round_index = int(row["round"]) - 1
        
        if round_index == 0:
            if row["winner"] == "draw":
                points[row["home_team_name"]][round_index] += 1
                points[row["away_team_name"]][round_index] += 1

            else:
                points[row["winner"]][round_index] += 3              

        else:
            if row["winner"] == "draw":
                points[row["home_team_name"]][round_index] = points[row["home_team_name"]][round_index - 1] + 1
                points[row["away_team_name"]][round_index] = points[row["away_team_name"]][round_index - 1] + 1

            else:
                points[row["winner"]][round_index] = points[row["winner"]][round_index - 1] + 3
                
                #managing the losing team
                if row["winner"] == row["home_team_name"]:
                    points[row["away_team_name"]][round_index] = points[row["away_team_name"]][round_index - 1]
                else:
                    points[row["home_team_name"]][round_index] = points[row["home_team_name"]][round_index - 1]
        
        
    #now we have to save the data on csv files!
    #print(points["Inter"], " Inter")
    #for each season we have, in dictionary points, the evolution of points per each team

    out_data = pd.DataFrame.from_dict(points, orient="index", columns=cols).reset_index()
    out_data = out_data.sort_values(by="round_38", ascending=False)

    out_path = "../data/season_points/" + str(season) + "-points.csv"

    out_data.to_csv(out_path)

    
