import urllib.request
import bs4

def parseDataTableFromHTML(url):
    html = urllib.request.urlopen(url) # retrieve html code from url
    soup = bs4.BeautifulSoup(html, 'html.parser') # create beautifulsoup object

    # get headers
    column_headers = [x.getText() for x in soup.findAll('tr', limit=2)[1].findAll('th')]

    # get our player data
    data_rows = soup.findAll('tr')[2:]

    return(column_headers, data_rows)

    # Turn yearly data into a DatFrame
    year_df = pd.DataFrame(player_data, columns=column_headers)
    
    # Append to the big dataframe
    draft_df = draft_df.append(year_df, ignore_index=True)
