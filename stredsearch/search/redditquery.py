from bs4 import BeautifulSoup
from django.http import JsonResponse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# MyPy is installed and has been run against this code - technically error checking in this way is unnecessary. As this isn't performance-optimised code, it doesn't hurt to include a belt-and-braces check.
def checkObjAndRaiseTypeError(test_obj: object, test_type, error_msg: str):
    if not isinstance(test_obj, test_type):
        raise TypeError(error_msg)


def checkStringAndRaiseValueError(test_string: str, test_value: str, error_msg: str):
    if test_string == test_value:
        raise ValueError(error_msg)


def buildTermsFromParams(q: str, search_type: str, limit: str) -> dict:
    checkObjAndRaiseTypeError(q, str, "q must be of type str")
    checkObjAndRaiseTypeError(search_type, str, "search_type must be of type str")
    checkObjAndRaiseTypeError(limit, str, "limit must be of type str")

    return {
        "q": q,
        "type": search_type,
        "limit": limit,
    }


def buildSubredFromParams(subreds: str) -> list:
    checkObjAndRaiseTypeError(subreds, str, "subreds must be of type str")

    subreds = subreds.replace(" ", "")

    if split_list := subreds.split(","):
        return split_list
    else:
        raise ValueError("subreds must contain at least one subreddit")


def buildUrl(terms: dict, subreddit: str = "") -> str:
    checkObjAndRaiseTypeError(terms, dict, "terms must be of type dict")
    checkObjAndRaiseTypeError(subreddit, str, "subreddit must be of type str")

    checkStringAndRaiseValueError(subreddit, "", "subreddit must not be empty string")
    checkStringAndRaiseValueError(
        terms["q"], "", "terms must contain a q parameter that is not empty string"
    )
    checkStringAndRaiseValueError(
        terms["type"],
        "",
        "terms must contain a type parameter that is not empty string",
    )
    checkStringAndRaiseValueError(
        terms["limit"],
        "",
        "terms must contain a limit parameter that is not empty string",
    )

    processed_terms = processTermsForUrl(terms)

    return f"https://www.reddit.com{subreddit}/search?{processed_terms}"


def processTermsForUrl(terms: dict) -> str:
    checkObjAndRaiseTypeError(terms, dict, "terms must be of type dict")

    terms_list = [f"{key}={term}" for key, term in terms.items()]
    return "&".join(terms_list)


def parseLinksFromHtml(html) -> list:
    soup = BeautifulSoup(html, "html5lib")

    extracted_tags = soup.find_all("a", attrs={"data-testid": "post-title"})

    if not isinstance(extracted_tags, list):
        raise TypeError("Error with BS4: Extracted_tags must be of type list")

    return generateRedditLinkDicts(extracted_tags)


def generateRedditLinkDicts(extracted_tags: list) -> list:
    checkObjAndRaiseTypeError(
        extracted_tags, list, "extracted_tags must be of type list"
    )

    links = []
    for tag in extracted_tags:
        tag_dict = {
            "question_title": tag["aria-label"],
            "question_link": f"https://www.reddit.com{tag['href']}",
        }
        links.append(tag_dict)

    return links


def getRedditHTMLViaSelenium(url: str) -> str:
    checkObjAndRaiseTypeError(url, str, "url must be of type str")

    checkStringAndRaiseValueError(url, "", "url must not be empty string")
    checkStringAndRaiseValueError(url, " ", "url must not be whitespace")

    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    except TimeOutException:
        raise TimeoutException("TimeoutException: Failed to load page")

    page_source = driver.page_source

    driver.quit()

    return page_source


def searchRedditAndReturnResponse(
    q: str, search_type: str, limit: str, subreddits: str
) -> JsonResponse:
    checkObjAndRaiseTypeError(q, str, "q must be of type str")
    checkObjAndRaiseTypeError(search_type, str, "search_type must be of type str")
    checkObjAndRaiseTypeError(limit, str, "limit must be of type str")
    checkObjAndRaiseTypeError(subreddits, str, "subreddits must be of type str")

    checkStringAndRaiseValueError(q, "", "q must not be empty string")
    checkStringAndRaiseValueError(
        search_type, "", "search_type must not be empty string"
    )
    checkStringAndRaiseValueError(limit, "", "limit must not be empty string")

    checkStringAndRaiseValueError(q, " ", "q must not be whitespace")
    checkStringAndRaiseValueError(
        search_type, " ", "search_type must not be whitespace"
    )
    checkStringAndRaiseValueError(limit, " ", "limit must not be whitespace")

    search_terms = buildTermsFromParams(q, search_type, limit)

    subreddit_list = buildSubredFromParams(subreddits)

    total_result_set = []

    for subred in subreddit_list:
        url = buildUrl(search_terms, f"/r/{subred}")

        html = getRedditHTMLViaSelenium(url)

        search_links = parseLinksFromHtml(html)

        total_result_set.extend(search_links)

    # response = JsonResponse(total_result_set, safe = False)
    # response.status_code = 201
    # print(response)
    return total_result_set
