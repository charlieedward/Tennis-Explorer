# USCID: 8747-1422-96
# NAME: KuoChen Huang

import pandas as pd
from playerH2H import get_h2h
from espn import get_most_GS, get_winner
from youtube import youtube_search

h2h = 'https://www.atptour.com/en/players/atp-head-2-head/'

if __name__ == "__main__":

    searching = True
    data = pd.read_csv("atpTop100.csv")

    while searching == True:
        category_selection = input(
            "What information do you want to search? (1) Player Ranking (2) Players Of Country (3) Player Records Of The Year (4) Player Age (5) H2H (6) Grand Slam (7) Youtube Video: ")
        # Search by Player Ranking
        if category_selection == '1':
            topNum = int(
                input("How many top players do you want to search?(ex.10): "))
            data.sort_values(by=['Ranking'], inplace=True)
            print(data[['Ranking', 'Player', 'Points']]
                  [:topNum].to_string(index=False))

        # Search by Player Country
        elif category_selection == '2':
            # to store all the countries in a list
            country_list = sorted(list(data['Country'].unique()))

            country_selection = input(
                "What information do you want to search further of countries?(1) Top100 Players (2) Top100 Players Count: ")
            if country_selection == '1':
                print("These are all the countries: " + str(country_list))
                country = input(
                    "Which country do you want to filter?(ex.USA): ")
                player_of_country = data[data['Country'] == country]
                print(player_of_country[['Ranking', 'Player']].to_string(
                    index=False))

            if country_selection == '2':
                country_count = int(
                    input("How many top cities do you want to search for?: "))
                print(data.groupby('Country').size().sort_values(
                    ascending=False).head(country_count))

        # Search by Player Records
        elif category_selection == '3':
            records_selection = input(
                "What information do you want to search?(1) Wins Count (2) Odds: ")
            player_count = int(
                input("How many top players do you want to search for?(ex.10): "))

            if records_selection == '1':
                data.sort_values(by=['Win'], ascending=False, inplace=True)
                print(data[['Ranking', 'Player', "Win"]]
                      [:player_count].to_string(index=False))

            if records_selection == '2':
                data.sort_values(by=['Odds'], ascending=False, inplace=True)
                print(data[['Ranking', 'Player', "Odds"]]
                      [:player_count].to_string(index=False))

        # Search by Player's Age
        elif category_selection == '4':
            sorting = input(
                "How do you want to sort?(1) Ascending (2) Descending: ")
            player_count = int(
                input("How many top players do you want to search for?(ex.10): "))

            if sorting == '1':
                data.sort_values(by=['Age'], inplace=True)
            if sorting == '2':
                data.sort_values(by=['Age'], ascending=False, inplace=True)

            print(data[['Ranking', 'Player', 'Age']]
                  [:player_count].to_string(index=False))

        # Search by Players h2h
        elif category_selection == '5':
            player_list = sorted(list(data['Player'].unique()))

            asklist = input(
                "Do you need the list of player's name in top100?(Yes/No): ")
            if asklist == 'Yes' or asklist == 'yes':
                print("These are all the players in top100: " + str(player_list))

            player1 = input(
                "Please enter player1's name(ex. Roger Federer): ")
            player2 = input(
                "Please enter player1's name(ex. Novak Djokovic): ")

            try:
                player1_code = data[data['Player'] == player1]['Code'].iloc[0]
                player1_name = "-".join(player1.lower().split(" "))
                player2_code = data[data['Player'] == player2]['Code'].iloc[0]
                player2_name = "-".join(player2.lower().split(" "))

                h2hurl = h2h + player1_name + "-vs-" + player2_name + \
                    '/' + player1_code + '/' + player2_code

                get_h2h(h2hurl)

            except:
                print("Can not find the player, please enter the name again!")

        # Search by GS
        elif category_selection == '6':
            grand_selection = input(
                "What information do you want to search for?(1) GS Counts Records (2) Winner of GS: ")
            if grand_selection == '1':
                number = int(
                    input("How many top ranked player do you want to search for?: "))
                get_most_GS(number)

            if grand_selection == '2':
                tournament_key = input(
                    "Which Tournament?(1) Australian Open (2) French Open (3) Wimbledon (4) U.S. Open: ")
                year = int(input("Winner of which year?(ex.2021): "))

                get_winner(tournament_key, year)

        # Search by YT Videos
        elif category_selection == '7':
            player = input(
                "Which player do you want to search for?:(ex. Roger federer) ")
            count = int(
                input("How many latest videos do you want to search?:(ex. 5) "))
            yt_df = youtube_search(player, count)
            yt_df = pd.DataFrame(yt_df, columns=['Player', 'Title', 'Link'])
            print(yt_df[['Title', 'Link']].to_string(index=False))

        else:
            print("Please choose again!")
            continue
        # Ask user to continue searching or not
        searching_check = input(
            "Do you want to continue searching? (Yes/No): ")

        if searching_check == 'Yes' or searching_check == 'yes':
            searching = True
        elif searching_check == 'No' or searching_check == 'no':
            searching = False
