# USCID: 8747-1422-96
# NAME: KuoChen Huang

import argparse
import datetime as dt
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import date
from datetime import datetime
import sys
DEVELOPER_KEY = "AIzaSyA1G8bTHc9D_kEbiWDQRm3j8HQIQ65dXn0"
youtube = build("youtube", "v3", developerKey=DEVELOPER_KEY)


def youtube_search(player, num):
    # today = date.today()
    # today_datetime = datetime(today.year, today.month, today.day)
    request_title = youtube.search().list(
        order="date",
        part="snippet",
        q=player,
        maxResults=num
    )
    request_link = youtube.search().list(
        order="date",
        part="id",
        q=player,
        maxResults=num)

    response_title = request_title.execute()
    response_link = request_link.execute()

    result = list()
    for i in range(len(response_title['items'])):
        # if dt.datetime.strptime(response['items'][i]['snippet']['publishTime'],'%Y-%m-%dT%H:%M:%SZ') > today_datetime:
        result.append([player, response_title['items'][i]['snippet']['title'],
                      'https://www.youtube.com/watch?v=' + response_link['items'][i]['id']['videoId']])
    print("Player: " + player + "'s videos have been scrapped!")
    # result[response_title['items'][i]['snippet']['title']
    # ] = 'https://www.youtube.com/watch?v=' + response_link['items'][i]['id']['videoId']

    return result
    # return(pd.DataFrame(result.items(), columns=['Title', 'Link']))


def show_scrap(atp_data, player_count):
    player_df = pd.DataFrame()
    for i in range(0, player_count):
        if i == 0:
            print("Start to Scrape Data!")
        yt_df = pd.DataFrame(youtube_search(atp_data['Player'][i], 5), columns=[
                             'Player', 'Title', 'Link'])
        player_df = pd.concat([player_df, yt_df], ignore_index=True)
    return player_df


if __name__ == "__main__":
    atp_data = pd.read_csv('atpTop100.csv')

    if len(sys.argv) == 1:
        df = show_scrap(atp_data, 10)
        df.to_csv('youtube.csv', index=False)
        print(df)
        print("All the data are stored into the file -> youtube.csv")

    elif len(sys.argv) == 2 and sys.argv[1] == '--scrape':
        print(show_scrap(atp_data, 1))

    elif len(sys.argv) == 3:
        filename = sys.argv[2]
        data = pd.read_csv(filename)
        print(data)
