from bs4 import BeautifulSoup
import requests
import json

url = 'https://mysingingmonsters.fandom.com/wiki/Island_Translations'

html = requests.get(url).content

soup = BeautifulSoup(html, 'html.parser')

table = soup.find('table')

trs = table.find_all('tr')[1:]

names = []

for tr in trs:
    tds = tr.find_all('td')

    names.append([td.text.strip() for td in tds[:3]])

with open('island_translations.json', 'w') as f:
    json.dump(names, f, indent=4)
