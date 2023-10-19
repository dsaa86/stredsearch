from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


def buildUrl(terms: dict, subreddit: str = '') -> str:

    processed_terms = processTermsForUrl(terms)


    return ("https://www.reddit.com" + subreddit + processed_terms)

def processTermsForUrl(terms: dict) -> str:
    last_key_in_dict = list(terms)[-1]

    processed_terms = '/search?'

    for key, term in terms.items():
        term_string = f"{key}={term}"
        
        if key != last_key_in_dict:
            term_string = term_string + "&"
        processed_terms = processed_terms + term_string

    return processed_terms

def parseLinksFromHtml(html: any) -> list:
    soup = BeautifulSoup(html, 'html5lib')

    extracted_tags = soup.find_all('a', attrs={'data-testid' : 'post-title'})

    formatted_search_results = generateRedditLinkTuples(extracted_tags)

    return formatted_search_results

def generateRedditLinkTuples(extracted_tags: any) -> list:
    link_tuples = []
    for tag in extracted_tags:
        tag_tuple = (tag['aria-label'], tag['href'])
        link_tuples.append(tag_tuple)

    return link_tuples

def searchRedditAndReturnResponse(terms: dict, subreddit: str = '') -> dict:
    url = buildUrl(terms, subreddit)
    
    options = Options()
    options.add_argument("--headless=new")
    
    driver = webdriver.Chrome(options = options)
    driver.get(url)

    time.sleep(5)

    html = driver.page_source

    search_links = parseLinksFromHtml(html)
    
    return search_links

terms = {
    'q' : 'exception raised during for loop python',
    'type' : 'link',
    'limit' : '100'
}

subred = '/r/python'

returned_terms = searchRedditAndReturnResponse(terms, subred)

for term in returned_terms:
    print(f"""{term}
""")