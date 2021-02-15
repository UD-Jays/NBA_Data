import requests
import bs4


# General function to parse out a list of tables from a block of HTML code
# Inputs: url (string)
# Outputs: html_tables (list)
def parseRegSeasonTable(url):

    html = requests.get(url) # retrieve html code from url
    if(html.status_code != 200): # status code = 200 for valid URLs
        print('URL incorrect') # if status code is not 200, end method
        return
    
    soup = bs4.BeautifulSoup(html.content, 'lxml') # create beautifulsoup object
    season = parseSeasonFromURL(url)
    
    # Parse out all of the <caption. tags in HTML, and specifically find the one titled {Season} Reagular Season Table
    # Then use BeautiFulSoup's find_parent function to pull the table where this caption appears, ie the Regular Season Table of stats
    for caption in soup.findAll('caption'):
        if(caption.getText() == (season + ' Regular Season Table')):
            regseason_table = caption.find_parent()

    return(regseason_table)


# Function to parse out the year (i.e. 2020) from the provided URL
# Inputs: url (string)
# Outputs: nba_season (string)
def parseSeasonFromURL(url):

    calendar_year = int(url[-4:]) # last 4 characters of url
    
    # Calendar year 2020 = NBA season 2019-20
    nba_season = str(calendar_year-1) + '-' + str(calendar_year)[-2:]

    return(nba_season)


# Function to parse out the column headers in the provided table
# Inputs: tbl (BeautifulSoup object)
# Outputs: column_headers (list of strings)
def parseHeadersFromTable(tbl):
    
    # table.find('tr') --> Only take the first row from the table, since table headers are repeated every 20 rows
    # .findAll('th') --> With that first row, parse out all of the table headers
    # [x.getText() for x in...] --> for each header returned by soup method, parse out just the text portion (leave behind styling)
    column_headers = [x.getText() for x in tbl.find('tr').findAll('th')]

    return(column_headers)


"""     # get headers
    column_headers = [x.getText() for x in soup.findAll('tr', limit=2)[1].findAll('th')]

    # get our player data
    data_rows = soup.findAll('tr')[2:]

    #return[column_headers, data_rows] """

"""     # Turn yearly data into a DataFrame
    year_df = pd.DataFrame(player_data, columns=column_headers)
    
    # Append to the big dataframe
    draft_df = draft_df.append(year_df, ignore_index=True) """

tbl = parseRegSeasonTable('https://www.basketball-reference.com/players/E/embiijo01/gamelog/2020')

headers = parseHeadersFromTable(tbl)

print(headers)