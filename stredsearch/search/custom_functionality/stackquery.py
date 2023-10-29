from typing import Type
import requests, json
from datetime import datetime
import zoneinfo
from django.utils.dateparse import parse_datetime

META_DATA = {
    "route_prepend": "https://api.stackexchange.com",
    "route_append": {
        "site": "stackoverflow",
    },
}

FILTERS = {
    "fromdate": "filter by oldest age of question",
    "todate": "filter by youngest age of question",
    "min": "filter by youngest possible age of question",
    "max": "filter by oldest possible age of question",
    "page": "the page number of results to show",
    "pagesize": "the number of results per page (max 100)",
    "order": {
        "asc": "order by ascending order",
        "desc": "order by descending order",
    },
    "sort": {
        "activity": "sort by recent activity",
        "votes": "sort by number of votes",
        "creation": "sort by creation date",
        "hot": "sort by current popularity of question",
        "week": "sort by creation week",
        "month": "sort by creation month",
    },
}

ACCESS_ROUTES = {
    "questions": {
        "question_by_tag": {
            "route": "/2.3/questions",
            "params": {
                "tagged": "tags that describe the question topic, e.g. 'python'",
            },
        },
        "related_questions": {
            "route": "/2.3/questions/{ids}/linked",
            "params": {
                "ids": "the id(s) of questions for which to find other, related questions",
                "test": "",
            },
        },
    },
    "search": {
        "search": {
            "route": "/2.3/search",
            "params": {
                "tagged": "the tags by which to search for questions",
                "nottagged": "tags of questions to be omitted from the search",
                "intitle": "text that should be present in the title of the question",
            },
        },
        "advanced-search": {
            "route": "/2.3/search/advanced",
            "params": {
                "q": "free form text",
                "accepted": "boolean - True returns only qs with accepted answers",
                "answers": "minimum number of answers a q must have received",
                "body": "text which must appear in question bodies",
                "closed": "True returns only closed questions, False returns only open qs, omitted returns any",
                "migrated": "True returns only qs migrated to another site, False returns only qs not migrated, omitted returns any",
                "notice": "True returns only qs with post notices, false returns only those without, omit returns any",
                "nottagged": "semicolon delimted list of tags, none will be present in q - must have at least one other parameter completed in order to be valid",
                "tagged": "semicolon delimted list of tags, at least one will be present in a w",
                "title": "text which must appear in q titles",
                "user": "the id of the user who must own the q",
                "url": "a url which must be returned in a post, may include wildcards",
                "views": "the minimum number of views returned qs must have",
                "wiki": "true returns only communited wiki qs, false returns only non-communited wiki qs, omit returns any",
            },
        },
    },
}

QUESTION_FIELDS = [
    "is_answered",
    "view_count",
    "answer_count",
    "score",
    "last_activity_date",
    "creation_date",
    "last_edit_date",
    "question_id",
    "link",
    "title",
]


def transposeKeyListForSerializer(category_list: list, key: str) -> list:

    if not isinstance(category_list, list):
        raise TypeError("category_list must be of type list")
    if not isinstance(key, str):
        raise TypeError("Key must be a string")
    if not all(isinstance(elem, str) for elem in category_list):
        raise TypeError("All elements in category_list must be of type string")

    transposed_list = []

    for elem in category_list:
        transposed_list.append({f"{key}": f"{elem}"})

    return transposed_list


def getQueryCategories() -> list:
    category_list = list(ACCESS_ROUTES.keys())
    category_list.pop(0)

    try:
        formatted_category_list = transposeKeyListForSerializer(category_list, "category")
    except TypeError as e:
        return {"error": f"Error: {e}"} 

    return formatted_category_list


def getQueryCategoryRoutes(category) -> list:
    route_list = list(ACCESS_ROUTES[category].keys())

    return transposeKeyListForSerializer(route_list, "route")


def processURLAndParamsToList(url, params: dict) -> list:

    params_string_for_return = ""

    for key in params.keys():
        print(key)
        params_string_for_return += key

    data_dict = {
        "url": url["url"],
        "params": params_string_for_return,
    }

    return [data_dict]


def getAPIRoute(category, query) -> str:
    api_route = ACCESS_ROUTES[category][query]["route"]
    return api_route


def getAPIParams(category, query) -> dict:
    return ACCESS_ROUTES[category][query]["params"]


def getRoutePrepend() -> str:
    return ACCESS_ROUTES["meta"]["route_prepend"]


def getRouteAppend() -> dict:
    return ACCESS_ROUTES["meta"]["route_append"]


def getDictOfPossibleFilters() -> dict:
    return ACCESS_ROUTES["meta"]["filters"]

def getFilters() -> dict:
    return ACCESS_ROUTES["meta"]["filters"]


def getOnlyQuestionsFromStackOverflowResponse(json_response: json) -> dict:

    if not isinstance(json_response, json):
        raise TypeError("json_response must be of type json")
    if "items" not in json_response.keys():
        raise KeyError("json_response must contain a key named 'items'")
    if not json_response["items"]:
        raise ValueError("json_response must contain a non-empty 'items' key")

    return json_response["items"]


def convertListToString(list_to_convert: list, delimiter: str = None) -> str:

    if not isinstance(list_to_convert, list):
        raise TypeError("list_to_convert must be of type list")
    if delimiter != None and not isinstance(delimiter, str):
        raise TypeError("delimiter must be of type string")

    return_string = ""
    for index, value in enumerate(list_to_convert):
        return_string += value
        if delimiter != None and index + 1 != len(list_to_convert):
            return_string += f"{delimiter} "

    return return_string


def convertMSToDateTime(ms_value: int) -> object:

    if not isinstance(ms_value, int):
        raise TypeError("ms_value must be of type int")

    converted_value = datetime.fromtimestamp(ms_value)
    converted_value = converted_value.strftime("%Y-%m-%d %H:%M:%S")
    converted_value = parse_datetime(converted_value)
    converted_value.replace(tzinfo=zoneinfo.ZoneInfo("Asia/Dubai"))
    return converted_value


def getQuestionData(question:dict) -> dict:

    if not isinstance(question, dict):
        raise TypeError("question must be of type dict")
    if "tags" not in question.keys():
        raise KeyError("question must contain a key named 'tags'")
    if "owner" not in question.keys():
        raise KeyError("question must contain a key named 'owner'")
    if not isinstance(question["tags"], list):
        raise TypeError("question['tags'] must be of type list")
    if not isinstance(question["owner"], dict):
        raise TypeError("question['owner'] must be of type dict")


    question_data = {}
    try:
        question_data['tags'] = convertListToString(question["tags"], ",")
    except TypeError as e:
        return {"error": f"Error: {e}"}


    # The owner data is stored as a nested dict within the parent question data
    for owner_data_key, owner_data_value in question["owner"].items():
        if owner_data_key == "user_id":
            question_data["user_id"] = owner_data_value
        if owner_data_key == "display_name":
            question_data["display_name"] = owner_data_value

    # Individual questions are not forced to have all fields present,
    # this logic prevents fields that aren't present in a question from
    # being appended as empty or raising an exception during runtime
    for key, data_field in question.items():
        if key in QUESTION_FIELDS:
            question_data[key] = question[key]

        # Serializer expects datetime, not timestamp as returned by SO
        if ( key in ["last_activity_date", "creation_date", "last_edit_date"] ):
            try:
                question_data[key] = convertMSToDateTime(question_data[key])
            except TypeError as e:
                return {"error": f"Error: {e}"}


def sanitiseStackOverflowResponse(json_response):

    if not isinstance(json_response, json):
        raise TypeError("json_response must be of type json")

    # full data set contains additional meta data that is unnecessary. This call strips away that meta data.
    try:
        complete_question_set = getOnlyQuestionsFromStackOverflowResponse(json_response)
    except (TypeError, KeyError, ValueError) as e:
        return {"error": f"Error: {e}"}

    sanitised_data = []

    for question in complete_question_set:
        try:
            sanitised_data.append(getQuestionData(question))
        except (TypeError, KeyError) as e:
            return {"error": f"Error: {e}"}

    return sanitised_data


def queryStackOverflow(category, query, filters) -> dict:
    route_prepend = getRoutePrepend()
    query_route = getAPIRoute(category, query)
    url = route_prepend + query_route["url"]
    params = filters

    params["site"] = getRouteAppend()["site"]

    try:
        query_response = requests.get(url, params)
    # Error raised typically when there is no internet connection on the client device
    except requests.exceptions.SSLError as e:
        return {"error": {
                    "SSLError": f"{e.strerror}"
                    }
                }
    except requests.exceptions.Timeout as e:
        return {"error": {
                    "Timeout": f"{e.strerror}"
                    }
                }
    except requests.exceptions.ConnectionError as e:
        return {"error": {
                    "ConnectionError": f"{e.strerror}"
                    }
                }
    except requests.exceptions.HTTPError as e:
        return {"error": {
                    "HTTPError": f"{e.strerror}"
                    }
                }
    except requests.exceptions.TooManyRedirects as e:
        return {"error": {
                    "TooManyRedirects": f"{e.strerror}"
                    }
                }
    except requests.exceptions.RequestException as e:
        return {"error": {
                    "RequestException": f"{e.strerror}"
                    }
                }

    json_response = json.loads(query_response.content)

    return sanitiseStackOverflowResponse(json_response)
