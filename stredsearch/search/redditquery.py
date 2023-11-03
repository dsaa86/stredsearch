import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys


def buildTermsFromParams(q: str, search_type: str, limit: str) -> dict:
    terms = {
        "q": f"{q}",
        "type": f"{search_type}",
        "limit": f"{limit}",
    }

    return terms

def buildSubredFromParams(subreds):
    return subreds.split(",")


def parseRedditSearchResults(search_results: dict) -> list:
    formatted_results_set = []

    for tuple in search_results:
        result = {"title": f"{tuple[0]}", "link": f"https://reddit.com{tuple[1]},"}
        formatted_results_set.append(result)

    return formatted_results_set















def buildUrl(terms: dict, subreddit: str = '') -> str:

    processed_terms = processTermsForUrl(terms)

    return f"https://www.reddit.com{subreddit}{processed_terms}"

def processTermsForUrl(terms: dict) -> str:
    last_key_in_dict = list(terms)[-1]

    processed_terms = '/search?'

    for key, term in terms.items():
        term_string = f"{key}={term}"
        
        if key != last_key_in_dict:
            term_string = f"{term_string}&"
        processed_terms = processed_terms + term_string

    return processed_terms

def parseLinksFromHtml(html: any) -> list:
    soup = BeautifulSoup(html, 'html5lib')

    extracted_tags = soup.find_all('a', attrs={'data-testid' : 'post-title'})

    return generateRedditLinkDicts(extracted_tags)


def generateRedditLinkDicts(extracted_tags: any) -> list:
    links = []
    for tag in extracted_tags:
        tag_dict = {"title" : tag['aria-label'], "link" : f"https://www.reddit.com{tag['href']}"}
        links.append(tag_dict)

    return links

def getRedditHTMLViaSelenium(url: str) -> str:
    options = Options()
    options.add_argument("--headless=new")
    
    driver = webdriver.Chrome(options = options)
    driver.get(url)

    time.sleep(2)

    return driver.page_source

def searchRedditAndReturnResponse(terms: dict, subreddit_list: list) -> dict:

    total_result_set = []

    for subred in subreddit_list:

        url = buildUrl(terms, f"/r/{subred}")
        
        html = getRedditHTMLViaSelenium(url)

        search_links = parseLinksFromHtml(html)
        
        total_result_set= total_result_set + search_links

    return total_result_set