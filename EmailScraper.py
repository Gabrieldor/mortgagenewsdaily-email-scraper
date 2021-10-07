import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd

#Initial Parameters
name_email = {}
#Create the UserAgent to simulate a Browser and pass that information to http header
ua = UserAgent()
header = {'User-Agent':str(ua.random)}
contentDiv = []

#Iterate over all 30 pages
for i in range(30):
    url = 'http://www.mortgagenewsdaily.com/directory/mortgage/california?PageIndex='+str(i)
    data = requests.get(url, headers=header).content
    soup = BeautifulSoup(data, features='lxml')
    mainDiv = soup.find_all('div', attrs={'class':'CommonContentBoxContent'})[1]
    contentDiv += mainDiv.find_all('div', attrs={'class':'BusinessListingUserContent'})

#Iterate over found divs
for content in contentDiv:
    a = content.find('div',attrs={'class':'ListingDisplayName'}).find('a',href=True)
    name = a.text
    url = f"http://www.mortgagenewsdaily.com{a['href']}"
    data = requests.get(url, headers=header).content
    soup = BeautifulSoup(data, features='lxml')

#Get div where we can find the emails
    try:
        text = soup.find_all('div',attrs={'class':'CommonContentBoxContent Contact'})[0].text.splitlines()
        for line in text:
            if '@' in line:
                email = line
                name_email[name]=[email]
                break
            else:
                name_email[name]=["This profile hasn't entered contact/email information."]
    except:
        name_email[name]=["This profile has been removed."]
        continue

#Convert the python dict to a Pandas dataframe and export it to csv
df = pd.DataFrame().from_dict(name_email).transpose()
df.columns=['Emails']
df.to_csv('Scraped Emails.csv')