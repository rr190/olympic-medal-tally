from bs4 import BeautifulSoup
import requests
import re
from collections import namedtuple
from typing import NamedTuple
import pandas as pd

# This is the URL that includes all links
# to all previous Summer Olympics medal tables
url = ("https://en.wikipedia.org/wiki/Category:Summer_Olympics_medal_tables")

html = requests.get(url).text
soup = BeautifulSoup(html, "html5lib")

# Retrieving URLs for each Summer Olympic Medal Tally
div_with_all_links = soup.find("div", {'class':'mw-category-group'})
all_links = ["https://en.wikipedia.org" + item['href'] for item in div_with_all_links('a')]

all_countries = []
all_years = []
all_golds = []
all_silvers = []
all_bronzes = []
all_totals = []

for link in all_links:
    # Goes through each link and retrieve the medal tally
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html5lib")

    regex = r"Summer Olympics medal table$"
    tables = soup("table")

    for i, table in enumerate(tables):
        test_string = table.find("caption")
        allMedalTable = []
        
        data = [i for i in table("tr")]

        test_data = data[0].find('th') #tests whether it is the correct table
        
        if test_data is not None and test_data.get_text().strip() == "Rank":
            year = int(link.split("/")[4][:4])
            print(year)
            #ignoring first and last row
            for i in range(1, len(data)-1):
                thead = data[i].find("th")
                country = data[i].find("a").get_text()
                

                #we only need the last 4
                idx = len(data[i].find_all("td")) - 4
                medals = [int(medal.get_text()) for medal in data[i].find_all("td")[idx:]]

                #adding the results
                all_years.append(year)
                all_countries.append(country)
                all_golds.append(medals[0])
                all_silvers.append(medals[1])
                all_bronzes.append(medals[2])
                all_totals.append(medals[3])

            break

result = {
    'Country': all_countries,
    'Years': all_years,
    'Gold': all_golds,
    'Silver': all_silvers,
    'Bronze': all_bronzes,
    'Total': all_totals
}

df = pd.DataFrame(result)

# saving the results into a CSV file
df.to_csv("medalTable.csv")