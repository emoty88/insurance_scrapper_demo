from .base_crawler import BaseCrawler

class MockIndemnity(BaseCrawler):
    def __init__(self, user_id):
        url = f'https://scraping-interview.onrender.com/mock_indemnity/{user_id}'
        super().__init__(url)
        self.data = {
            'customer':{},
            'agent': {},
            'policies': []
        }
        self.file_name = 'mock_indemnity.json'
    
    def run(self):
        print('start crawling')
        self.get_customer()
        self.get_agent()
        self.get_policies()

        self.print_data()
        self.save()
    
    def get_agent(self):
        agent_soup = self.soup.find('div', {'class': 'agent-detail'})
        self.data['agent'] = {
            'name': agent_soup.find('dd', {'class':'value-name'}).text,
            'producer_name': agent_soup.find('dd', {'class':'value-producerCode'}).text,
            'agency_name': agent_soup.find('dd', {'class':'value-agencyName'}).text,
            'agency_code': agent_soup.find('dd', {'class':'value-agencyCode'}).text,
        }
    
    def get_customer(self):
        customer_soup = self.soup.find('div', {'class': 'customer-detail'})
        self.data['customer'] = {
            'name': customer_soup.find('dd', {'class':'value-name'}).text,
            'producer_name': customer_soup.find('dd', {'class':'value-id'}).text,
            'agency_name': customer_soup.find('dd', {'class':'value-email'}).text,
            'agency_code': customer_soup.find('dd', {'class':'value-address'}).text,
        }
    
    def get_policies(self):
        policy_soup = self.soup.find('ul', {'class', 'policy-ul'})
        policy_items = policy_soup.find_all('li', {'class','list-group-item'})
        for pi in policy_items:
            policy = {
                'id': pi.find('span', {'class', 'id value-holder'}).text,
                'premium':  pi.find('span', {'class', 'premium value-holder'}).text,
                'status':  pi.find('span', {'class', 'status value-holder'}).text,
                'effective_date':   pi.find('span', {'class', 'effectiveDate value-holder'}).text,
                'termination_date':  pi.find('span', {'class', 'terminationDate value-holder'}).text,
                'last_payment_date': pi.find('span', {'class', 'lastPaymentDate value-holder'}).text,
            }
            self.data['policies'].append(policy)
            

        
        
        
        

    

        