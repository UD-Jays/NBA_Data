import sys
import urllib.request
import bs4
import pandas as pd

url_template = "http://www.basketball-reference.com/draft/NBA_{year}.html"

draft_df = pd.DataFrame()

for year in range(1966, 2015):
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

draft_df.to_csv("draft_data_1966_to_2014.csv")



""" url = "http://www.basketball-reference.com/draft/NBA_2014.html"

html = urlopen(url)

soup = BeautifulSoup(html, "html.parser")

column_headers = [x.getText() for x in soup.findAll('tr', limit=2)[1].findAll('th')] # our column headers
column_headers.pop(0)

data_rows = soup.findAll('tr')[2:]   # skip the first 2 header rows

# player_data = [[x.getText() for x in data_rows[i].findAll('td')] for i in range(len(data_rows))]

player_data = []  # create an empty list to hold all the data

for i in range(len(data_rows)):  # for each table row
    player_row = []  # create an empty list for each pick/player

    # for each table data element from each table row
    for td in data_rows[i].findAll('td'):        
        # get the text content and append to the player_row 
        player_row.append(td.getText())        

    # then append each pick/player to the player_data matrix
    player_data.append(player_row)


df = pd.DataFrame(player_data, columns=column_headers)

df.head()  # head() lets us see the 1st 5 rows of our DataFrame by default

df = df[df.Player.notnull()]

df.rename(columns={'WS/48':'WS_per_48'}, inplace=True)

# get the column names and replace all '%' with '_Perc'
df.columns = df.columns.str.replace('%', '_Perc')


# Get the columns we want by slicing the list of column names
# and then replace them with the appended names
df.columns.values[14:18] = [df.columns.values[14:18][col] + "_per_G" for col in range(4)]

df = df.apply(pd.to_numeric, errors="ignore")

df = df[:].fillna(0) # index all the columns and fill in the 0s

df.loc[:,'Yrs':'AST'] = df.loc[:,'Yrs':'AST'].astype(int)

df.head() # All NaNs are now replaced with 0s

df.insert(0, 'Draft_Yr', 2014) """