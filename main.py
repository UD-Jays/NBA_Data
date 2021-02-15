import sys
import urllib.request
import bs4
import pandas as pd

url_template = "http://www.basketball-reference.com/draft/NBA_{year}.html"

draft_df = pd.DataFrame()

for year in range(1966, 2020):
    url = url_template.format(year=year)
    
    html = urllib.request.urlopen(url)
    soup = bs4.BeautifulSoup(html, 'html.parser') # create our BS object

    column_headers = [x.getText() for x in soup.findAll('tr', limit=2)[1].findAll('th')] # our column headers
    column_headers.pop(0)

    # get our player data
    data_rows = soup.findAll('tr')[2:] 
    player_data = [[td.getText() for td in data_rows[i].findAll('td')] for i in range(len(data_rows))]

    # Turn yearly data into a DatFrame
    year_df = pd.DataFrame(player_data, columns=column_headers)
    # create and insert the Draft_Yr column
    year_df.insert(0, 'Draft_Yr', year)
    
    # Append to the big dataframe
    draft_df = draft_df.append(year_df, ignore_index=True)

# Convert data to proper data types
draft_df = draft_df.apply(pd.to_numeric, errors="ignore")

# Get rid of the rows full of null values
draft_df = draft_df[draft_df.Player.notnull()]

# Replace NaNs with 0s
draft_df = draft_df.fillna(0)

# Rename Columns
draft_df.rename(columns={'WS/48':'WS_per_48'}, inplace=True)
# Change % symbol
draft_df.columns = draft_df.columns.str.replace('%', '_Perc')
# Add per_G to per game stats
draft_df.columns.values[15:19] = [draft_df.columns.values[15:19][col] + 
                                  "_per_G" for col in range(4)]

# Changing the Data Types to int
draft_df.loc[:,'Yrs':'AST'] = draft_df.loc[:,'Yrs':'AST'].astype(int)

draft_df.isnull().sum() # No missing values in our DataFrame

#draft_df.to_csv("draft_data_1966_to_2020.csv")