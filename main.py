import requests
from bs4 import BeautifulSoup
import requests_cache

requests_cache = requests_cache.install_cache('cache')

page = r'https://leagueoflegends.fandom.com/wiki/List_of_champions'

class IMDBScraper():
    def __init__(self, url):
        self.url = url
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.text, 'html.parser')
    
    def get_title(self):
        return self.soup.find('h1', id='firstHeading').text.strip()

    def get_description(self):
        return self.soup.find('div', class_='mw-parser-output').find('p').text.strip()

    def get_summary(self):
        arr = []
        summary_links = self.soup.find_all('li', class_='toclevel-1')
        for link in summary_links:
            item = {
                'link': self.url + link.find('a')['href'],
                'title': link.find('a').text
                }
            print(item)
            arr.append(item)
        return arr
    
    def get_scrapped_champions(self):
        list_items = self.soup.find('div', class_='columntemplate').find('ul').find_all('li')
        arr = []

        for item in list_items:
            item = {
                'link': "https://leagueoflegends.fandom.com" + item.find('a')['href'],
                'title': item.find('a')['title']
            }
            arr.append(item)
            print(item)

        return arr

    def get_champions(self):
        rows = self.soup.find('table', class_='article-table sticky-header sortable').find('tbody').find_all('tr')
        del rows[0]
        champions = []
        for row in rows:
            data = row.find_all('td')
            if(data[4].find('span') != None and data[5].find('span')!= None):
                champion = {
                    'img': data[0].find('img')['data-src'],
                    'name': data[0].find('span', class_='champion-icon').find('a')['title'].replace('/LoL', ''),
                    'classes': data[1]['data-sort-value'],
                    'class_link': "https://leagueoflegends.fandom.com" + data[1].find('a')['href'],
                    'release_date': data[2].text.replace('\n', ''),
                    'last_changed': data[3].find('a').text,
                    'version_link': "https://leagueoflegends.fandom.com" + data[3].find('a')['href'],
                    'blue_essence': data[4].find('span').text,
                    'rp': data[5].find('span').text,
                }
                print(champion)
                champions.append(champion)
        return champions

    def print_all(self):
        print(self.get_title(), self.get_description(), sep='\n\n\n')
        self.get_summary()
        self.get_scrapped_champions()
        self.get_champions()

IMDBScraper(page).print_all()