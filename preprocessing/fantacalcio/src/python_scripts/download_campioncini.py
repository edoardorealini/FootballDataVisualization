from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import pandas as pd
# from tqdm import tqdm

parent_folder = Path.cwd().parent

filename = parent_folder / "data/stats2020.csv"

# read the columns of players' names
all_names = pd.read_csv(filename)["Nome"]

file = open("no_img.txt", "w")

for player_name in all_names:

    if " " in player_name:
        player_name = player_name.replace(" ", "-")
    if "\'" in player_name:
        player_name = player_name.replace("\'", "-")
    if "." in player_name:
        player_name = player_name.replace(".", "")

    img_name = player_name + ".png"

    url = "https://content.fantacalcio.it/web/campioncini/medium/" + img_name

    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urlopen(req, timeout=200).read()
        save_folder = parent_folder / "data/campioncini/"
        img_save = save_folder / img_name

        output = open(img_save, "wb")
        output.write(response)
        output.close()

    except (HTTPError, URLError) as e:
        file.write("Player: " + player_name + " not found. \tReason: " + e.reason + "\n")
        continue

file.close()
