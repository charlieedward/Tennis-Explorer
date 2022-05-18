# USCID: 8747-1422-96
# NAME: KuoChen Huang

import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup

h2h = 'https://www.atptour.com/en/players/atp-head-2-head/'

# Function Definition


def get_h2h(url):

    content = requests.get(url)
    soup = BeautifulSoup(content.content, 'html.parser')

    left_player = soup.find("div", attrs={"class": "h2h-player-left"})
    left_player_name = left_player.find("span", attrs={"class": "first-name"}).text.strip(
    ) + " " + left_player.find("span", attrs={"class": "last-name"}).text.strip()

    left_player_wins = left_player.find(
        "div", attrs={"class": "players-head-rank"}).text.strip()
    left_player_odds = left_player.find(
        "div", attrs={"class": "players-head-rank-text"}).text.strip().split(" ")[0]

    right_player = soup.find("div", attrs={"class": "h2h-player-right"})
    right_player_name = right_player.find("span", attrs={"class": "first-name"}).text.strip(
    ) + " " + right_player.find("span", attrs={"class": "last-name"}).text.strip()
    right_player_wins = right_player.find(
        "div", attrs={"class": "players-head-rank"}).text.strip()
    right_player_odds = right_player.find(
        "div", attrs={"class": "players-head-rank-text"}).text.strip().split(" ")[0]

    data = [[left_player_name, left_player_wins, left_player_odds],
            [right_player_name, right_player_wins, right_player_odds]]

    h2h_df = pd.DataFrame(data, columns=['Player', 'Wins', 'Win Percentage'])
    print(h2h_df)
