from retriever_library import filter_fixtures_by_status_and_next_n
from retriever_library import get_predictions_by_fixture_ids
from retriever_library import get_fixtures_by_league
import json

'''
get_current_leagues("test_leagues.json")
filter_leagues_by_country("test_leagues.json", "italian_leagues.json", "Italy")

with open("../data/italian_leagues.json", ) as italian_leagues:
    italian_leagues_json = json.load(italian_leagues)
    league_ids = []

    for league in italian_leagues_json:
        league_ids.append(league["league_id"])
        #print(league["league_id"])

    print(league_ids[:3])
'''



get_fixtures_by_league(dest_filename="all_serieA_fixtures.json", 
                        league_id=2857)
filter_fixtures_by_status_and_next_n(fixtures_filename="all_serieA_fixtures.json", 
                                    dest_filename="next_NS_10_serieA.json", 
                                    status_list=["NS", "TBD"],next_n= )

with open("../data/next_NS_10_serieA.json", ) as fixtures:
    fixtures_json = json.load(fixtures)
    fixture_ids = []

    for fixture in fixtures_json:
        fixture_ids.append(fixture["fixture_id"])

    get_predictions_by_fixture_ids(dest_filename="pred_next10_fix_serieA.json",fixture_ids=fixture_ids)
