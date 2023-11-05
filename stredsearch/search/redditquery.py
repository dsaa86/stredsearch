import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys


def buildTermsFromParams(q: str, search_type: str, limit: str) -> dict:

    if not isinstance(q, str):
        raise TypeError("q must be of type str")
    if not isinstance(search_type, str):
        raise TypeError("search_type must be of type str")
    if not isinstance(limit, str):
        raise TypeError("limit must be of type str")

    return {
        "q": f"{q}",
        "type": f"{search_type}",
        "limit": f"{limit}",
    }


def buildSubredFromParams(subreds: str) -> list:

    if not isinstance(subreds, str):
        raise TypeError("subreds must be of type str")
    
    subreds = subreds.replace(" ", "")

    if split_list := subreds.split(","):
        return split_list
    else:
        raise ValueError("subreds must contain at least one subreddit")


# def parseRedditSearchResults(search_results: dict) -> list:


#     if not isinstance(search_results, dict):
#         raise TypeError("search_results must be of type dict")
    

#     formatted_results_set = []

#     for tuple in search_results:
#         result = {"title": f"{tuple[0]}", "link": f"https://reddit.com{tuple[1]},"}
#         formatted_results_set.append(result)

#     return formatted_results_set


def buildUrl(terms: dict, subreddit: str = '') -> str:

    if not isinstance(terms, dict):
        raise TypeError("terms must be of type dict")
    if not isinstance(subreddit, str):
        raise TypeError("subreddit must be of type str")
    
    if subreddit == '':
        raise ValueError("subreddit must not be empty string")
    
    if terms["q"] == '':
        raise ValueError("terms must contain a q parameter")
    if terms["type"] == '':
        raise ValueError("terms must contain a type parameter")
    if terms["limit"] == '':
        raise ValueError("terms must contain a limit parameter")
    
    if terms["q"] is None:
        raise ValueError("terms must contain a q parameter")
    if terms["type"] is None:
        raise ValueError("terms must contain a type parameter")
    if terms["limit"] is None:
        raise ValueError("terms must contain a limit parameter")

    processed_terms = processTermsForUrl(terms)

    return f"https://www.reddit.com{subreddit}{processed_terms}"


def processTermsForUrl(terms: dict) -> str:

    if not isinstance(terms, dict):
        raise TypeError("terms must be of type dict")

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

    if not isinstance(extracted_tags, list):
        raise TypeError("Error with BS4: Extracted_tags must be of type list")

    return generateRedditLinkDicts(extracted_tags)


def generateRedditLinkDicts(extracted_tags: list) -> list:

    if not isinstance(extracted_tags, list):
        raise TypeError("extracted_tags must be of type list")
    
    links = []
    for tag in extracted_tags:
        tag_dict = {"title" : tag['aria-label'], "link" : f"https://www.reddit.com{tag['href']}"}
        links.append(tag_dict)

    return links


def getRedditHTMLViaSelenium(url: str) -> str:

    if not isinstance(url, str):
        raise TypeError("url must be of type str")
    
    if url == '':
        raise ValueError("url must not be empty string")
    
    if url == " ":
        raise ValueError("url must not be whitespace")

    options = Options()
    options.add_argument("--headless=new")
    
    driver = webdriver.Chrome(options = options)
    driver.get(url)

    time.sleep(2)

    return driver.page_source


def searchRedditAndReturnResponse(q: str, search_type: str, limit: str, subreddits: str) -> dict:

    if not isinstance(q, str):
        raise TypeError("q must be of type str")
    if not isinstance(search_type, str):
        raise TypeError("search_type must be of type str")
    if not isinstance(limit, str):
        raise TypeError("limit must be of type str")
    if not isinstance(subreddits, str):
        raise TypeError("subreddits must be of type str")
    
    if q == '':
        raise ValueError("q must not be empty string")
    if search_type == '':
        raise ValueError("search_type must not be empty string")
    if limit == '':
        raise ValueError("limit must not be empty string")
    
    if q == " ": 
        raise ValueError("q must not be whitespace")
    if search_type == " ":
        raise ValueError("search_type must not be whitespace")
    if limit == " ":
        raise ValueError("limit must not be whitespace")

    search_terms = buildTermsFromParams(q, search_type, limit)

    subreddit_list = buildSubredFromParams(subreddits)

    total_result_set = []

    for subred in subreddit_list:

        url = buildUrl(search_terms, f"/r/{subred}")
        
        html = getRedditHTMLViaSelenium(url)

        search_links = parseLinksFromHtml(html)
        
        total_result_set= total_result_set + search_links

    return total_result_set