# USCID: 8747-1422-96
# NAME: KuoChen Huang

import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import sys

columns_name = ["Year", "Tournament", "winner", "runnerup"]


def get_grandslam(*argv):
    url = "http://www.espn.com/tennis/history"
    content = requests.get(url)
    soup = BeautifulSoup(content.content, 'html.parser')
    all_record = list()
    content = soup.find("table", attrs={"class": "tablehead"})

    # define the pattern and scrape range
    if argv[0] == '--scrape':
        num = 7
    elif argv[0] == 'all':
        num = len(content.find_all("tr"))

    # to trace the status
    count = 1

    for i in range(2, num):
        temp = list()
        if count == 1:
            print("Start to Scrape Data!")
        elif count % 100 == 0:
            print("Have scraped " + str(count) + " rows of data!")

        for j in range(len(content.find_all("tr")[i].find_all("td"))):
            temp.append(content.find_all("tr")[
                        i].find_all("td")[j].text.strip())
        all_record.append(temp)
        count += 1
        # print(content.find_all("tr")[i].text.strip())
        # test.append(content.find_all("tr")[i].text.strip())
    # all_Record = content.find_all("tr")[2]
    return all_record


def get_most_GS(num):

    grandSlam_df = pd.read_csv('grand_slam.csv')
    sortlist = grandSlam_df['winner'].value_counts()
    print(sortlist[:num])


def get_winner(tournament_key, year):

    grandSlam_df = pd.read_csv('grand_slam.csv')
    tounament_list = {'1': 'Australian Open',
                      '2': 'French Open', '3': 'Wimbledon', '4': 'U.S. Open'}
    print(grandSlam_df[(grandSlam_df['Tournament'] == tounament_list[tournament_key]) & (
        grandSlam_df['Year'] == year)]['winner'].values[0])


if __name__ == "__main__":
    if len(sys.argv) == 1:
        data = get_grandslam('all')
        grandSlam_df = pd.DataFrame(data, columns=columns_name)
        grandSlam_df.to_csv('grand_slam.csv', index=False)
        print(grandSlam_df)
        print("All the data are stored into the file -> grand_slam.csv")

    elif len(sys.argv) == 2:
        pattern = sys.argv[1]
        data = get_grandslam(pattern)
        grandSlam_df = pd.DataFrame(data, columns=columns_name)
        print(grandSlam_df)

    elif len(sys.argv) == 3:
        filename = sys.argv[2]
        data = pd.read_csv(filename)
        print(data)
