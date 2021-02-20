import pandas as pd
import htmlParser as hp


# Function to build player home page URL
# Inputs: PlayerName (string)
# Outputs: url (string)
# EX: https://www.basketball-reference.com/players/e/embiijo01.html
def getPlayerPageURL(PlayerName):

    url_template = "https://www.basketball-reference.com/players/{lastInit}/{lastName5}{firstName2}01.html"

    firstName = PlayerName.split()[0].lower()
    lastName = PlayerName.split()[1].lower()

    url = url_template.format(lastInit=lastName[0], lastName5=lastName[0:5], firstName2=firstName[0:2])

    return(url)



def getPlayerHomePage(PlayerName):

    # parse HTML table using function built in htmlParser.py
    url = getPlayerPageURL(PlayerName)
    table_name = 'Per Game Table'
    
    HTML_tbl = hp.parseTableFromHTML(url, table_name)
    
    if(HTML_tbl == None):
        return
    else:
        column_headers = hp.parseHeadersFromTable(HTML_tbl)
        #column_headers.pop(0) # get ride of 'Rank' column
    
        data_rows = hp.parseDataFromTable(HTML_tbl)

        # build pandas dataframe to hold game log stats, using parsed info
        activeSeasons_df = pd.DataFrame(data_rows, columns=column_headers)

        return(activeSeasons_df)


x = getPlayerHomePage('Joel Embiid')
