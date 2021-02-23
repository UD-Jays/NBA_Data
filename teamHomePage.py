import pandas as pd
import htmlParser as hp

# Function to build Team:URL dictionary
# Inputs: none
# Outputs: {Team Name (string): url extension (string)} (dictionary)
# EX: {'Philadelphia 76ers': '/teams/PHI/', 'Phoenix Suns': '/teams/PHO/'}
def getFranchiseList():
    # basketball-reference teams index page = https://www.basketball-reference.com/teams/
    active_franchises_url = 'https://www.basketball-reference.com/teams/'
    active_franchises_tbl_name = 'Active Franchises Table'
    active_franchises_tbl = hp.parseTableFromHTML(active_franchises_url, active_franchises_tbl_name)

    # Parse out table rows, dropping first row which is headers
    # class = full_table filters out archived franchises i.e. Philadelphia Warriors
    rows = active_franchises_tbl.findAll('tr', class_="full_table")
  
    team_names = []
    team_urls = []
    for i in range(len(rows)):
        temp_name = rows[i].find('th').getText()
        temp_url = rows[i].find('a', href=True).get('href')

        team_names.append(temp_name)
        team_urls.append(temp_url)

    # Creates a dictionary where first element of team_names corresponds with first element of team_urls and so on
    franchise_dict = dict(zip(team_names, team_urls))
    
    return(franchise_dict)


# Function to get Team Home Page URL for team name passed to method
# Inputs: Team Name (string)
# Outputs: url (string)
# EX: https://www.basketball-reference.com/teams/PHI/
def getTeamHomePageURL(TeamName):

    url_template = "https://www.basketball-reference.com/{team_URL}"

    team_URL = getFranchiseList()[TeamName]

    url = url_template.format(team_URL = team_URL)

    return(url)


x = getTeamHomePageURL('Philadelphia 76ers')
print(x)