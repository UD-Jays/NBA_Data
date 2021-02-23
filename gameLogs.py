import pandas as pd
import htmlParser as hp


# Function to convert a calendar year (i.e. 2020) to the related NBA season (i.e. 2019-20)
# Inputs: Year (string)
# Outputs: nba_season (string)
def getNBASeason(Year):
    
    # Calendar year 2020 = NBA season 2019-20
    nba_season = str(int(Year)-1) + '-' + Year[-2:]

    return(nba_season)


# Function to build game log URL for a player name + season
# Inputs: PlayerName (string), Season (string)
# Outputs: url (string)
# EX: https://www.basketball-reference.com/players/e/embiijo01/gamelog/2020
def getGameLogURL(PlayerName, Season):

    url_template = "http://www.basketball-reference.com/players/{lastInit}/{lastName5}{firstName2}01/gamelog/{year}"

    firstName = PlayerName.split()[0].lower()
    lastName = PlayerName.split()[1].lower()

    url = url_template.format(lastInit=lastName[0], lastName5=lastName[0:5], firstName2=firstName[0:2], year=Season)

    return(url)


# Function to build pandas dataframe of stats for specific player, specific season
# Inputs: PlayerName (string), Year (string, ex: '2020')
# Outputs: seasonLog_df (pandas dataframe)
def getGameLogsSeason(PlayerName, Year):

    # parse HTML table using function built in htmlParser.py
    url = getGameLogURL(PlayerName, Year)
    table_name = getNBASeason(Year) + ' Regular Season Table'
    
    HTML_tbl = hp.parseTableFromHTML(url, table_name)
    
    if(HTML_tbl == None):
        return(None)
    else:
        column_headers = hp.parseHeadersFromTable(HTML_tbl)
    
        data_rows = hp.parseDataFromTable(HTML_tbl)

        # build pandas dataframe to hold game log stats, using parsed info
        seasonLog_df = pd.DataFrame(data_rows, columns=column_headers)
        seasonLog_df = seasonLog_df[seasonLog_df.Rk != 'Rk']
        seasonLog_df = seasonLog_df.drop(columns='Rk')
        seasonLog_df = seasonLog_df[seasonLog_df.G != '']

        return(seasonLog_df)


# Function to build pandas dataframe to hold stats for specific player, entire career
# Career = 1900 to present
# Inputs: PlayerName (string, ex: 'Joel Embiid')
# Outputs: careerLog_df (pandas dataframe)
def getGameLogsCareer(PlayerName):

    careerLog_df = pd.DataFrame()
    
    for year in range(2010, 2021):
        season_df = getGameLogsSeason(PlayerName, str(year))
        if(season_df is not None):
            if(len(season_df.columns) >= 29):
                careerLog_df = careerLog_df.append(season_df, ignore_index=True)

    return(careerLog_df)



def plotSixersGameLogs(Year);
    
embiid_df = getGameLogsCareer('Joel Embiid')