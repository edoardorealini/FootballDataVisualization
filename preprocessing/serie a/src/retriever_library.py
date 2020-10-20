import requests
import json
import pandas as pd

data_path = "../data/"
base_url = "https://api-football-v1.p.rapidapi.com/v2"

headers = {
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
    'x-rapidapi-key': "8e365a2420msh9e37db3a35f23eep1b14fdjsn9ee9e26c21b6"
    }


'''
This following function, loads the list of Serie A league_ids from the csv file "serieA_seasons_full.csv"
and retrieves for each season (league_id) the list of the 20 top players. 
The results are written into one json and csv file per each request
'''
def get_top_scoreres():
    df = pd.read_csv("../data/serieA_seasons_full.csv")
    league_ids = df["league_id"].to_list()

    path = "/topscorers/"
    season = 2010

    for league in league_ids:
        url = base_url + path + str(league)

        print("[GetTopScorers] Getting top scorers of league: ", league)
        response = requests.request("GET", url, headers=headers)

        with open(data_path + "/players/top-seasonal/topscorers-" + str(season) + ".json", "w") as out_file:
            print("[GetTopScorers] Writing on the output json file!")
            json.dump(response.json()["api"]["topscorers"], out_file, indent=4)

        print("[GetTopScorers] Converting in CSV format!")

        #this method is broken, better to do it manually as alwaysor find another way.
        #csv_converter = pd.read_json(data_path + "/players/top-seasonal/topscorers-" + str(season) + ".json")
        #csv_converter.to_csv(data_path + "/players/top-seasonal/topscorers-" + str(season) + ".csv")
        
        json_data = response.json()
        data = []
        
        for player in json_data["api"]["topscorers"]:
            data.append((
                player["player_id"],
                player["player_name"],
                player["firstname"],
                player["lastname"],
                player["position"],
                player["nationality"],
                player["team_id"],
                player["team_name"],
                player["games"]["appearences"],
                player["games"]["minutes_played"],
                player["goals"]["total"],
                player["goals"]["assists"],
                player["goals"]["conceded"],
                player["goals"]["saves"],
                player["shots"]["total"],
                player["shots"]["on"],
                player["penalty"]["won"],
                player["penalty"]["commited"],
                player["penalty"]["success"],
                player["penalty"]["missed"],
                player["penalty"]["saved"],
                player["cards"]["yellow"],
                player["cards"]["second_yellow"],
                player["cards"]["red"]
            ))

        out_df = pd.DataFrame(data, columns=["player_id", 
                                            "player_name", 
                                            "firstname", 
                                            "lastname", 
                                            "position",
                                            "nationality",
                                            "team_id",
                                            "team_name",
                                            "appearences",
                                            "minutes_played",
                                            "total_goals",
                                            "assists_goals",
                                            "conceded_goals",
                                            "saves_goals",
                                            "total_shots",
                                            "on_shots",
                                            "won_penalty",
                                            "commited_penalty",
                                            "success_penalty",
                                            "missed_penalty",
                                            "saved_penalty",
                                            "yellow_cards",
                                            "second_yellow_cards",
                                            "red_cards"])

        out_df.to_csv(data_path + "/players/top-seasonal/topscorers-" + str(season) + ".csv")

        print("[GetTopScorers] Converted to CSV, going on.")

        season += 1



'''
This function  converts the data coming from the api in json format
into a plain CSV
'''
def fixtures_stats_csv_generator(input_file_json, out_file_csv_path):

    inp_data = open(data_path + input_file_json, )
    fixtures_json = json.load(inp_data)

    print("Converting file ", data_path + input_file_json)

    #in this list there will be touples, each touple represents a row of the dataset
    data = []

    for fixture in fixtures_json["api"]["fixtures"]:
        data.append((
            fixture["fixture_id"],
            fixture["league_id"],
            fixture["event_date"],
            fixture["event_timestamp"],
            fixture["round"],
            fixture["status"],
            fixture["statusShort"],
            fixture["homeTeam"]["team_id"],
            fixture["homeTeam"]["team_name"],
            fixture["awayTeam"]["team_id"],
            fixture["awayTeam"]["team_name"],
            fixture["goalsHomeTeam"],
            fixture["goalsAwayTeam"]
        ))

    df = pd.DataFrame(data, columns=   ["fixture_id", "league_id", "event_date", "event_timestamp", 
                                        "round", "status", "status_short", "home_team_id", "home_team_name", 
                                        "away_team_id", "away_team_name", "goals_home_team", "goals_away_team"])
    df.to_csv(out_file_csv_path)


'''
This function gets the league_id from csv file serieA_seasons.csv
and for each one of the seasons gets the teams, and dumps into 
a csv file the statistics for that season.
'''
def get_oldTeams_statistics(leagues_list, season):
    #seasons_df = pd.read_csv(data_path + "serieA_seasons_last.csv")
    #seasons_df.to_html("temp.html")
    #leagues_list = seasons_df["league_id"].to_list()

    file_name = "serieA_statistics_"
    #season = 2017
    #path to get teams by league, then parse the json and create
    #the csv with the data that we need
    teams_path = "/teams/league/" 
    stats_path = "/statistics/"

    for league in leagues_list:
        path = teams_path + str(league)
        url = base_url + path
        try:
            response = requests.request("GET", url, headers=headers)
            teams_json = response.json()

            teamsid_list = []

            for team in teams_json["api"]["teams"]:
                teamsid_list.append((team["team_id"], team["name"]))

        except:
            print("Error calling the list of teams for season ", season)
        #now in teamsid_list we have the ids of teams fot the league
        #and the team name as tuples

        #now for each team for this league we have to get the stats
        final_data = []
        for tup in teamsid_list:
            path = stats_path + str(league) + "/" + str(tup[0])
            url = base_url + path
            try:
                response = requests.request("GET", url, headers=headers)
                print(url, season)
                response_json = response.json()
                stats = response_json["api"]["statistics"]
                matches = stats["matchs"]
                goals = stats["goals"]
                goals_avg = stats["goalsAvg"]

                final_data.append(
                    (   tup[0], tup[1], 
                        matches["matchsPlayed"]["total"],
                        matches["wins"]["total"],
                        matches["draws"]["total"],
                        matches["loses"]["total"],
                        goals["goalsFor"]["total"],
                        goals["goalsAgainst"]["total"],
                        goals_avg["goalsFor"]["total"],
                        goals_avg["goalsAgainst"]["total"]
                    )
                )
            except:
                print("ERROR with team ", tup[0], " in season ", season)
                print("Response is:")
                print(json.dumps(response_json, indent=4))
        
        final_df = pd.DataFrame(final_data, columns=["team_id", "team_name", "matches_played", "wins", "draws", "loses", "goalsFor", "goalsAgainst", "avg_goalsFor", "avg_goalsAgainst"])

        final_df.to_csv(data_path + "team_stats/" + file_name + str(season) + ".csv")

        season = season + 1



# seasons available endpoint
def get_seasonAvailable_by_league(dest_filename, league_id):
    path = "/leagues/seasonsAvailable/"
    url = base_url + path +  str(league_id)

    print(url)

    print("[GetSAByLeague] Launching API request")
    response = requests.request("GET", url, headers=headers)

    print("[GetSAByLeague] API request ok!")
    print("[GetSAByLeague] Opening output file: " + data_path + dest_filename)

    with open(data_path + dest_filename, "w") as out_file:
        print("[GetSAByLeague] Writing on the output file!")
        #out_file.write(json.dump(response.json()))
        json.dump(response.json(), out_file, indent=4)

    print("[GetSAByLeague] Done!")

def get_leagues_by_search(dest_filename, search_name):
    path = "/leagues/search/"
    url = base_url + path +  str(search_name)

    print(url)

    print("[GetLeaguesBySearch] Launching API request")
    response = requests.request("GET", url, headers=headers)

    print("[GetLeaguesBySearch] API request ok!")
    print("[GetLeaguesBySearch] Opening output file: " + data_path + dest_filename)

    with open(data_path + dest_filename, "w") as out_file:
        print("[GetLeaguesBySearch] Writing on the output file!")
        #out_file.write(json.dump(response.json()))
        json.dump(response.json(), out_file, indent=4)

    print("[GetLeaguesBySearch] Done!")

'''
Gets the statistics of team team_id from league league_id (note that the league id is linked to the year!)
'''
def get_team_statistics(dest_filename, team_id, league_id):
    api_path = "/statistics/"
    url = base_url + api_path + str(league_id) + "/" + str(team_id)

    print("[GetTeamStats] Launching API request")
    response = requests.request("GET", url, headers=headers)

    print("[GetTeamStats] API request ok!")
    print("[GetTeamStats] Opening output file: " + data_path + dest_filename)

    with open(data_path + dest_filename, "w") as out_file:
        print("[GetTeamStats] Writing on the output file!")
        #out_file.write(json.dump(response.json()))
        json.dump(response.json(), out_file, indent=4)

    print("[GetTeamStats] Done!")


'''
Gets the statistics of team team_id from league league_id until specified date
Date format: YYYY-MM-DD
'''
def get_team_statistics_date(dest_filename, team_id, league_id, year):
    api_path = "/statistics/"
    url = base_url + api_path + str(league_id) + "/" + str(team_id) + "/" + str(year)

    print("[GetTeamStats] Launching API request")
    response = requests.request("GET", url, headers=headers)

    print("[GetTeamStats] API request ok!")
    print("[GetTeamStats] Opening output file: " + data_path + dest_filename)

    with open(data_path + dest_filename, "w") as out_file:
        print("[GetTeamStats] Writing on the output file!")
        #out_file.write(json.dump(response.json()))
        json.dump(response.json(), out_file, indent=4)

    print("[GetTeamStats] Done!")


'''
Given a league_id (and a destination filename)  obtains a json with all the teams of such league.
We are interested in getting the list of team_id to later retrieve all the statistics!
'''
def get_teams_from_league(dest_filename, league_id):
    api_path = "/teams/league/"
    url = base_url + api_path + str(league_id)

    print("[GetTeamsFromLeague] Launching API request")
    response = requests.request("GET", url, headers=headers)

    print("[GetTeamsFromLeague] API request ok!")
    print("[GetTeamsFromLeague] Opening output file: " + data_path + dest_filename)

    with open(data_path + dest_filename, "w") as out_file:
        print("[GetTeamsFromLeague] Writing on the output file!")
        #out_file.write(json.dump(response.json()))
        json.dump(response.json(), out_file, indent=4)

    print("[GetTeamsFromLeague] Done!")


def get_current_leagues(dest_filename):
    current_leagues = "/leagues/current"
    url = base_url + current_leagues

    print("[GetAllCurrentLeagues] Launching API request")
    response = requests.request("GET", url, headers=headers)

    print("[GetAllCurrentLeagues] API request ok!")
    print("[GetAllCurrentLeagues] Opening output file: " + data_path + dest_filename)

    with open(data_path + dest_filename, "w") as out_file:
        print("[GetAllCurrentLeagues] Writing on the output file!")
        #out_file.write(json.dump(response.json()))
        json.dump(response.json(), out_file, indent=4)

    print("[GetAllCurrentLeagues] Done!")


def get_fixtures_by_league(dest_filename, league_id):
    fixtures_by_leagueid = "/fixtures/league/" + str(league_id)
    url = base_url + fixtures_by_leagueid

    print("[GetFixturesByLeague] Getting fixtures of league: " + str(league_id))
    response = requests.request("GET", url, headers=headers)

    print("[GetFixturesByLeague] Writing on output file: " + data_path + dest_filename)
    with open(data_path + dest_filename, "w") as out_file:
        json.dump(response.json(), out_file, indent=4)

    print("[GetFixturesByLeague] Done!")


def get_predictions_by_fixture_ids(dest_filename, fixture_ids): #NB fixture_ids is a list
    
    predictions = []

    print("[GetPredictionsByFixtureId] Opening output file: " + dest_filename)
    with open(data_path + dest_filename, "w") as out_file:
        for fixture in fixture_ids:
            url = base_url + "/predictions/" + str(fixture)
            print("[GetPredictionsByFixtureId] Retrieving predictions for fixture " + str(fixture))
            response = requests.request("GET", url, headers=headers)
            response = response.json()
            response["api"]["predictions"][0]["fixture_id"] = fixture
            predictions.append(response["api"]["predictions"])
        
        print("[GetPredictionsByFixtureId] Writing output file")
        #out_file.write(str(predictions))
        json.dump(predictions, out_file, indent=4)
    
    print("[GetPredictionsByFixtureId] Done!")
    
    
def filter_leagues_by_season(leagues_filename, dest_filename, season):
    print("[FilterLeaguesBySeason] Opening input file: " + data_path + leagues_filename)
    input_file = open(data_path + leagues_filename, )
    print("[FilterLeaguesBySeason] Opening output file: " + data_path + dest_filename)
    out_file = open(data_path + dest_filename, "w")

    print("[FilterLeaguesBySeason] Loading json data")
    json_data = json.load(input_file)

    result = []

    print("[FilterLeaguesBySeason] Filtering leagues of season " + str(season))
    for league in json_data["api"]["leagues"]:
        if league["season"] == season:
            #out_file.write(json.dumps(league))
            result.append(league)
    
    json.dump(result, out_file, indent=4)
    out_file.close()
    print("[FilterLeaguesBySeason] Done!")


def filter_leagues_by_country(leagues_filename, dest_filename, country):
    print("[FilterLeaguesByCountry] Opening input file: " + data_path + leagues_filename)
    input_file = open(data_path + leagues_filename, )
    print("[FilterLeaguesByCountry] Opening output file: " + data_path + dest_filename)
    out_file = open(data_path + dest_filename, "w")

    print("[FilterLeaguesByCountry] Loading json data")
    json_data = json.load(input_file)

    result = []

    print("[FilterLeaguesByCountry] Filtering leagues of country " + str(country))
    for league in json_data["api"]["leagues"]:
        if league["country"] == country:
            result.append(league)
            #out_file.write(json.dumps(league))
    
    json.dump(result, out_file, indent=4)
    out_file.close()
    print("[FilterLeaguesByCountry] Done!")

def filter_leagues_by_season_and_country(leagues_filename, dest_filename, season, country):
    print("[FilterLeaguesByCountry] Opening input file: " + data_path + leagues_filename)
    input_file = open(data_path + leagues_filename, )
    print("[FilterLeaguesByCountry] Opening output file: " + data_path + dest_filename)
    out_file = open(data_path + dest_filename, "w")

    print("[FilterLeaguesByCountry] Loading json data")
    json_data = json.load(input_file)

    result = []

    print("[FilterLeaguesByCountry] Filtering leagues of season " + str(season) + " and country " + country)
    for league in json_data["api"]["leagues"]:
        if league["country"] == country and league["season"] == season:
            result.append(league)
            #out_file.write(json.dumps(league))
    
    json.dump(result, out_file, indent=4)
    out_file.close()
    print("[FilterLeaguesByCountry] Done!")


def filter_fixtures_by_status(fixtures_filename, dest_filename, status_list):
    print("[FilterFixturesByStatus] Loading fixtures from: " + data_path + fixtures_filename)
    fixtures_file = open(data_path + "serieA_fixtures.json",)

    print("[FilterFixturesByStatus] Loading json data")
    json_fixtures = json.load(fixtures_file)
    fixtures = json_fixtures["api"]["fixtures"]

    result = []

    print("[FilterFixturesByStatus] Filtering and writing on file!")
    print("[FilterFixturesByStatus] Statuses to select: ", status_list)
    with open(data_path + dest_filename, "w") as out_file:
        for fix in fixtures:
            if fix["statusShort"] in status_list:
                result.append(fix)

        #out_file.write(str(result))
        json.dump(result, out_file, indent=4)

    print("[FilterFixturesByStatus] Done!")


def filter_fixtures_by_next_n(fixtures_filename, dest_filename, next_n):
    print("[FilterFixturesByNextN] Loading fixtures from: " + data_path + fixtures_filename)
    fixtures_file = open(data_path + "serieA_fixtures.json",)

    print("[FilterFixturesByNextN] Loading json data")
    json_fixtures = json.load(fixtures_file)
    fixtures = json_fixtures["api"]["fixtures"]

    result = []
    counter = 0

    print("[FilterFixturesByNextN] Filtering and writing on file!")
    print("[FilterFixturesByNextN] Getting next " + str(next_n) + " fixtures")
    with open(data_path + dest_filename, "w") as out_file:
        for fix in fixtures and counter < next_n:
            result.append(fix)
            counter = counter + 1

        #out_file.write(str(result))
        json.dump(result, out_file, indent=4)

    print("[FilterFixturesByNextN] Done!")


def filter_fixtures_by_status_and_next_n(fixtures_filename, dest_filename, status_list, next_n):
    print("[FilterFixturesByStatusAndNextN] Loading fixtures from: " + data_path + fixtures_filename)
    fixtures_file = open(data_path + "serieA_fixtures.json",)

    print("[FilterFixturesByStatusAndNextN] Loading json data")
    json_fixtures = json.load(fixtures_file)
    fixtures = json_fixtures["api"]["fixtures"]

    #print(fixtures) DEBUG

    result = []
    counter = 0

    print("[FilterFixturesByStatusAndNextN] Filtering and writing on file!")
    print("[FilterFixturesByStatusAndNextN] Statuses to select: ", status_list)
    with open(data_path + dest_filename, "w") as out_file:
        for fix in fixtures:
            if fix["statusShort"] in status_list and counter < next_n:
                result.append(fix)
                #print(fix)
                counter = counter + 1

        #out_file.write(str(result))
        json.dump(result, out_file, indent=4)

    print("[FilterFixturesByStatusAndNextN] Done!")   