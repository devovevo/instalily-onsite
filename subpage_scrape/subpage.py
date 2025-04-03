import requests, random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from common import DUMMY_USER_AGENTS

def scrape(url: str):
    headers = {
        'User-Agent': random.choice(DUMMY_USER_AGENTS)
		}
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, features="html.parser")
    b = soup.find('body')
    
    if b and b.stripped_strings:
        list_of_strings = [s for s in b.stripped_strings]
    else:
        list_of_strings = []

    links = list({ 
		urljoin(url, a.get('href')) 
		for a in soup.find_all('a') 
		if a.get('href') and a.get('href')[:4] == "http" and a.get('href').split("/")[2] == url.split("/")[2] and not(a.get('rel') and 'nofollow' in a.get('rel'))
	})
    
    return list_of_strings, links