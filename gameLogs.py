import pandas as pd
import htmlParser as hp

# Create a URL template for scraping stats for any player, any season
# EX: https://www.basketball-reference.com/players/e/embiijo01/gamelog/2020
url_template = "http://www.basketball-reference.com/players/{lastInit}/{lastName5}{firstName2}01/gamelog/{year}"

playerStats_df = pd.DataFrame()

# Creates a pandas dataframe of stats for specific player, specific season
# Inputs: PlayerName (string, ex: 'Joel Embiid'), Season_Year (string, ex: '2020')
def getGameLogsSeason(PlayerName, Season):
    firstName = PlayerName.split()[0]
    lastName = PlayerName.split()[1]

    url = url_template.format(lastInit=lastName[0], lastName5=lastName[0:5], firstName2=firstName[0:2], year=Season)

    # build data frame to hold game logs for entire season
    seasonLog_df = pd.DataFrame()

    # extract HTML table using function built in htmlParser.py
    [column_headers, bulk_data] = hp.parseDataTableFromHTML(url)

    # extract individual game logs from table
    # <td> = HTML tag for cell in table
    game_stats = [[td.getText() for td in bulk_data[i].findAll('td')] for i in range(len(bulk_data))]

    # build data frame to hold player's game logs for season
    seasonLog_df = pd.DataFrame(game_stats, columns=column_headers)

    return(seasonLog_df)

getGameLogsSeason('Joel Embiid', '2020')