from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

url = "http://www.basketball-reference.com/draft/NBA_2014.html"

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
print(df.dtypes)