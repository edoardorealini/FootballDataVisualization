import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt

data_path = "./data/"

# utils functions

def convert(lst): 
    lst = np.array(lst) 
    return list(-lst)


def difference(lst1, lst2):
    diff = []
    diff_zip = zip(lst1, lst2)
    for i,j in diff_zip:
        diff.append(i-j)
    return diff


def addition(lst1, lst2):
    diff = []
    diff_zip = zip(lst1, lst2)
    for i,j in diff_zip:
        diff.append(i+j)
    return diff


def division(lst1, lst2):
    div = []
    div_zip = zip(lst1, lst2)
    for i,j in div_zip:
        div.append(i/j)
    return div
    

def difference_pos_neg(lst):
    diff_pos, diff_neg = [], []
    for el in lst:
        if (el > 0):
            diff_pos.append(el)
            diff_neg.append(0)
        else:
            diff_pos.append(0)
            diff_neg.append(-el)
    return diff_pos, diff_neg


def colorscale_to_rgb(lst, colorscale):
    rgb_list = []
    max_n = max(lst)
    min_n = min(lst)
    cmap = plt.cm.get_cmap(colorscale)
    for el in lst:
        normalized = (el-min_n)/(max_n-min_n)
        rgba = cmap(normalized)
        rgba = tuple(int((255*x)) for x in rgba[0:3])
        rgba = 'rgb' + str(rgba)
        rgb_list.append(rgba)
    return rgb_list


def get_teams_dict_list():

    all_teams = []

    for season in range(2010, 2020):
        df = pd.read_csv(data_path + "/teams/" + str(season) + ".csv")

        teams = df["team_name"].to_list()

        for team in teams:
            all_teams.append(team)

    all_teams_unique = list(set(all_teams))

    all_teams_dict_list = []

    for team in all_teams_unique:
        d = {
            "label": team,
            "value": team
        }

        all_teams_dict_list.append(d)

    return all_teams_dict_list