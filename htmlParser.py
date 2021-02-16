import requests
import bs4


# General function to parse out a specified table from block of HTML
# Uses <table> attribute 'caption' to specify table name
# Inputs: url (string), table_name (string)
# Outputs: html_tables (list)
def parseTableFromHTML(url, table_name):

    html = requests.get(url) # retrieve html code from url
    if(html.status_code != 200): # status code = 200 for valid URLs
        print('URL incorrect') # if status code is not 200, end method
        return
    
    soup = bs4.BeautifulSoup(html.content, 'lxml') # create beautifulsoup object
    
    # Parse out all of the <caption. tags in HTML, and specifically find the one titled {Season} Reagular Season Table
    # Then use BeautiFulSoup's find_parent function to pull the table where this caption appears, ie the Regular Season Table of stats
    # If no table is found with table_name, None is returned
    table = None
    for caption in soup.findAll('caption'):
        if(caption.getText() == table_name):
            table = caption.find_parent()

    return(table)


# Function to parse out the column headers in the provided table
# Inputs: tbl (BeautifulSoup object)
# Outputs: column_headers (list of strings)
def parseHeadersFromTable(tbl):

    # tbl.find('tr') --> Only take the first row from the table, since table headers are repeated every 20 rows
    # .findAll('th') --> With that first row, parse out all of the table headers
    # [x.getText() for x in...] --> for each header returned by findAll('th'), parse out just the text portion (leave behind styling)
    column_headers = [x.getText() for x in tbl.find('tr').findAll('th')]

    return(column_headers)


# Function to parse out rows of data in the provided table
# Inputs: tbl (BeautifulSoup object)
# Outputs: data_rows (list of lists)
def parseDataFromTable(tbl):
    
    #parse out all rows in tbl, skipping first row since this is the header row
    rows = tbl.findAll('tr')[1:]

    # [[]... for i in range(len(rows))] --> loop through every row of data in table, storing individual row data in its own list, and the group of rows in an outer list
    # row[i].findAll('td') --> for each row [i] in list of rows, find all cells tagged by <td>
    # [x.getText() for x in...] --> for each table cell returned by findAll('td'), parse out just the text portion (leave behind styling)
    data = [[x.getText() for x in rows[i].findAll('td')] for i in range(len(rows))]


    return(data)