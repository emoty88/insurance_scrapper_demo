import json
from .base_crawler import BaseCrawler

class PlaceholderCarrier(BaseCrawler):
    def __init__(self, user_id):
        self.host = 'https://scraping-interview.onrender.com'
        self.url = f'{self.host}/placeholder_carrier/{user_id}'

        super().__init__(self.url)
        self.data = {
            'customer':{},
            'agent': {},
            'policies': []
        }

        self.file_name = 'placeholder_carrier.json'

    
    def run(self):
        self.get_customer()
        self.get_agent()
        self.get_policies()

        self.print_data()
        self.save()
    
    def get_agent(self):
        agent_data = self.soup.find('div', {'class':'agency-details'})
        info_lines = agent_data.find_all('div', {'class':'nice-formatted-kv'})
        self.data['agent'] = {
            'name':info_lines[0].find('span').text,
            'producer_name': info_lines[1].find('span').text,
            'agency_name': info_lines[2].find('span').text,
            'agency_code': info_lines[3].find('span').text,
        }

    def get_customer(self):
        customer_data = self.soup.find('div', {'class':'customer-details'})
        cus_info_lines = customer_data.find('div', {'class':'card-body'}).find_all('div')
        self.data['customer'] = {
            'name':cus_info_lines[0].find('span').text,
            'id':cus_info_lines[1].find('span').text,
            'email': customer_data.find('div', {'class':'card-body'}).text.split(':')[4].replace('Address',''),
            'address':cus_info_lines[3].text
        }
    
    def get_policies(self):
        placeholder_carrier_policy = PlaceholderCarrierPolicy(self.url)
        self.data['policies'] = placeholder_carrier_policy.run()


class PlaceholderCarrierPolicy(BaseCrawler):
    def __init__(self, url):
        self.host = 'https://scraping-interview.onrender.com'
        super().__init__(url)
        self.policies = []
    
    def run(self):
        self.get_policy_data()
        print(len(self.policies))
        return self.policies
        

    def get_policy_data(self):
        # Getting Policies 
        policy_soup = self.soup.find('div', {'class':'policy-details'})
        self.table = policy_soup.find('table')
        policy_rows = self.table.find_all('tr',{'class':'policy-info-row'})
        for policy_row in policy_rows:
            policy = {
                'id': policy_row.find_all('td')[0].text,
                'premium': policy_row.find_all('td')[1].text,
                'status': policy_row.find_all('td')[2].text,
                'effective_date':  policy_row.find_all('td')[3].text,
                'termination_date': policy_row.find_all('td')[4].text,
                'last_payment_date':'',
            }
            self.policies.append(policy)
        
        next_page = self.check_next_page()
        print('asd')
        if next_page:
            # Get next page and recursivly call this function to get all pages
            self.create_soup(next_page)
            print(next_page)
            next_page_data = self.get_policy_data()
            print(next_page_data)
            # self.policies = self.policies + next_page_data

    def check_next_page(self):

        # Check Get paging links
        links = self.table.find('tfoot').find_all('a')
        print(links)
        for l in links:
            # checking both link if Next > is a then return the link
            print(l.text)
            if l.text == 'Next >':
                return f"{self.host}{l['href']}"
        
        # If could not find a link with Next > text retrun fals to stop recursice loop
        return False
