import json
from bs4 import BeautifulSoup
import requests


class BaseCrawler():
    def __init__(self, url=None):
        # create default session,
        # Using Session because be able to use Cookies, HeaderAuth, sessions etc
        self.file_name = 'crawler_data.json'
        self.data = {}
        self.s = requests.session()

        # Soup object to parse page
        self.soup = None

        if (url):
            self.create_soup(url)
        else:
            print('url must spescified.')
    
    def create_soup(self, url):
        page = self.s.get(url)
        # print('Getting page: ', page.request.url)
        # Check response status for network issue or other potencial problems
        if page.ok:
            self.soup = BeautifulSoup(page.content, 'html.parser')
        else:
            print(f'Request failed. Status Code: {page.status_code}')
        
    def run(self):
        # Crawler method...
        print('Run Method not implemented!!!')

    def print_data(self):
        print(self.data)
    
    def save(self):
        with open(self.file_name, 'w') as file:
            json.dump(self.data, file, indent=4)
        

        