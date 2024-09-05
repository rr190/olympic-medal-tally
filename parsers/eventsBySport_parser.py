from bs4 import BeautifulSoup
import requests
import pandas as pd

# all of the years of Summer Olympics
all_years = [1896]
for i in range(1900, 1916, 4):
    all_years.append(i)
for i in range(1920, 1940, 4):
    all_years.append(i)
for i in range(1948, 2028, 4):
    all_years.append(i)


res_sports = [] #sports type
res_n = [] #number of events under the sport type
res_years = [] #year

# loop through each year
for year in all_years:
    print("Parsing Summer Olympics " + str(year), end="\r")

    # get the HTML using BeautifulSoup
    url  = 'https://en.wikipedia.org/wiki/' + str(year) + '_Summer_Olympics'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')

    # focusing on the events
    div = soup.find('div', {'class': 'div-col'})
    lis = list(div.find('ul').children)

    # loop through <li> tags
    for li in lis:
        if li.find('li') == None:
            #if we can find numbers beside the sports
            if li.find('small'):
                n = int(li.find('small').get_text().strip('()'))

                # adding into our data
                res_n.append(int(n))
                res_sports.append(li.find('a').get_text())
                res_years.append(int(year))


        #if there are multiple sports under the current sport
        elif li.get_text() != '\n':
            
            #if we can find numbers beside the sports
            if li.find('small'):
                n = 0
                for x in li.find_all('small'):
                    n += int(x.get_text().strip('()'))

                # adding into our data
                res_n.append(int(n))
                res_sports.append(li.get_text().split("\n")[0].strip())
                res_years.append(int(year))


# Put all data into a DataFrame                
res = {
    "year": res_years,
    "sport_type": res_sports,
    "event_count": res_n,
}
df = pd.DataFrame(res)

# saving the results by converting DataFrame into a CSV file
df.to_csv("eventsBySport.csv")



