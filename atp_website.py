# USCID: 8747-1422-96
# NAME: KuoChen Huang

import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import sys


url = 'https://www.atptour.com/en/rankings/singles'
h2h = 'https://www.atptour.com/en/players/atp-head-2-head/'
header_list = ['Ranking', 'Country', 'Player',
               'Player_Page', 'Age', 'Points', 'Win', 'Loss', 'Odds']

# Create a handle, page, to handle the contents of the website
page = requests.get(url)
# Store the contents of the website under doc
doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')

# Function Definition


def get_record(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.content, 'html.parser')

    content = soup.find("div", attrs={"class": "main-content"})
    Win_Loss_Of_Year = content.find_all("td", attrs={"colspan": "1"})[2].find(
        "div", attrs={"class": "stat-value"}).text.strip()
    Win_Of_Year = int(Win_Loss_Of_Year.split('-')[0])
    Loss_Of_Year = int(Win_Loss_Of_Year.split('-')[1])
    return Win_Of_Year, Loss_Of_Year


def get_tennis(*argv):
    data = list()
    header_list = list()
    content = requests.get(url)
    soup = BeautifulSoup(content.content, 'html.parser')

    table = soup.find_all("table", attrs={"class": "mega-table"})
    body = table[0].findAll("tr")

    # find the header of the table
    for col in body[0].find_all("th"):
        header_list.append(col.text.strip())

    # define the pattern and scrape range
    if argv[0] == '--scrape':
        scrape_data = body[1:6]
    elif argv[0] == 'all':
        scrape_data = body[1:]

    # to trace the status
    count = 1

    # find the data
    for item in scrape_data:
        # to trace the status and print to user every ten rows
        if count == 1:
            print("Start to Scrape Data!")
        elif count % 20 == 0:
            print("Have scraped " + str(count) + " rows of data!")

        rank = item.find("td", attrs={"class": "rank-cell"}).text.strip()
        country = item.find(
            "td", attrs={"class": "country-cell"}).find("img").get('alt')
        player = item.find("td", attrs={"class": "player-cell"}).text.strip()
        player_infopg = 'https://www.atptour.com/' + \
            item.find("td", attrs={"class": "player-cell"}).find('a')['href']
        age = item.find("td", attrs={"class": "age-cell"}).text.strip()
        points = item.find(
            "td", attrs={"class": "points-cell"}).text.strip().replace(',', '')
        # get their records of this season
        win, loss = get_record(player_infopg)
        odds = win/(win+loss)
        data.append([int(rank), country, player, player_infopg,
                    int(age), int(points), win, loss, odds])
        count += 1

    return data


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


if __name__ == "__main__":

    if len(sys.argv) == 1:
        web_data = get_tennis('all')
        df = pd.DataFrame(columns=header_list, data=web_data)
        # create a new column 'Code' for h2h searching
        df['Code'] = df['Player_Page'].apply(lambda x: x.split('/')[-2])

        # write the dataframe to csv file
        df.to_csv('atpTop100.csv', index=False)
        print(df)
        print("All the data are stored into the file -> atpop100.csv")

    elif len(sys.argv) == 2:
        pattern = sys.argv[1]
        web_data = get_tennis(pattern)
        df = pd.DataFrame(columns=header_list, data=web_data)
        # create a new column 'Code' for h2h searching
        df['Code'] = df['Player_Page'].apply(lambda x: x.split('/')[-2])
        print(df)

    elif len(sys.argv) == 3:
        filename = sys.argv[2]
        data = pd.read_csv(filename)
        print(data)
        print("File: " + filename + "has been imported!")
