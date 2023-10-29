import json
import zoneinfo
from datetime import datetime
from typing import Type

import requests
from django.utils.dateparse import parse_datetime
from models import *

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










def queryStackOverflow(category, query, filters) -> dict:
    route_prepend = getRoutePrepend()
    query_route = getAPIRoute(category, query)
    url = route_prepend + query_route
    params = filters
    params["site"] = getRouteAppend()

    try:
        query_response = requests.get(url, params)
    # Error raised typically when there is no internet connection on the client device
    except requests.exceptions.SSLError as e:
        return { "error": { "SSLError": f"{ e.strerror }" } }
    except requests.exceptions.Timeout as e:
        return { "error": { "Timeout": f"{ e.strerror }" } }
    except requests.exceptions.ConnectionError as e:
        return { "error": { "ConnectionError": f"{ e.strerror }" } }
    except requests.exceptions.HTTPError as e:
        return { "error": { "HTTPError": f"{ e.strerror }" } }
    except requests.exceptions.TooManyRedirects as e:
        return { "error": { "TooManyRedirects": f"{ e.strerror }" } }
    except requests.exceptions.RequestException as e:
        return { "error": { "RequestException": f"{ e.strerror }" } }

    json_response = json.loads(query_response.content)

    return sanitiseStackOverflowResponse(json_response)


def getRoutePrepend() -> str:
    prepend = StackRouteMeta.objects.get(pk=1)
    return prepend['route_prepend']


def getAPIRoute(category, query) -> str:
    return StackRoute.objects.get(route_category=category, route_query=query)


def getRouteAppend() -> str:
    append = StackRouteMeta.objects.get(pk=1)
    return append['route_append']


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


def getOnlyQuestionsFromStackOverflowResponse(json_response: json) -> dict:

    if not isinstance(json_response, json):
        raise TypeError("json_response must be of type json")
    if "items" not in json_response.keys():
        raise KeyError("json_response must contain a key named 'items'")
    if not json_response["items"]:
        raise ValueError("json_response must contain a non-empty 'items' key")

    return json_response["items"]


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
    
    try:
        question_data["user_id"] = extractOwnerData(question, "user_id")
        question_data["display_name"] = extractOwnerData(question, "display_name")
    except TypeError as e:
        return { "error": { "TypeError": f"{ e.strerror }" } }
    except KeyError as e:
        return { "error": { "KeyError": f"{ e.strerror }" } }
    except ValueError as e:
        return { "error": { "ValueError": f"{ e.strerror }" } }

    # Individual questions are not forced to have all fields present,
    # this logic prevents fields that aren't present in a question from
    # being appended as empty or raising an exception during runtime
    question_data_fields_for_question = extractRelevantQuestionDataFieldsForQuestion(question)
    question_data |= question_data_fields_for_question
    return question_data


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


def extractOwnerData(question: dict, key: str) -> str:

    if not isinstance(question, dict):
        raise TypeError("question must be of type dict")
    if not isinstance(key, str):
        raise TypeError("key must be of type str")
    if "owner" not in question.keys():
        raise KeyError("question must contain a key named 'owner'")
    if not isinstance(question["owner"], dict):
        raise TypeError("question['owner'] must be of type dict")
    if key not in question["owner"].keys():
        raise KeyError(f"question['owner'] must contain a key named '{key}'")
    if not isinstance(question["owner"][key], str):
        raise TypeError(f"question['owner']['{key}'] must be of type str")
    if key not in ["user_id", "display_name"]:
        raise ValueError("key must be one of the following: 'user_id', 'display_name'")

    for owner_data_key, owner_data_value in question["owner"].items():
        if owner_data_key == "user_id" and key == "user_id":
            return owner_data_value
        if owner_data_key == "display_name" and key == "display_name":
            return owner_data_value
        

def extractRelevantQuestionDataFieldsForQuestion(question: dict) -> dict:
    all_possible_question_data_fields = getQuestionDataFields()
    matched_data_fields = {}
    for key, _ in question.items():
        if key in all_possible_question_data_fields:
            matched_data_fields[key] = question[key]

        # Serializer expects datetime, not timestamp as returned by SO
        if ( key in ["last_activity_date", "creation_date", "last_edit_date"] ):
            try:
                matched_data_fields[key] = convertMSToDateTime(matched_data_fields[key])
            except TypeError as e:
                return {"error": { "TypeError" : f"{ e.strerror }" } }
    return matched_data_fields


def getQuestionDataFields() -> list:
    data_fields_from_db = StackQuestionDataFields.objects.all()
    return [field.data_field_name for field in data_fields_from_db]


def convertMSToDateTime(ms_value: int) -> object:

    if not isinstance(ms_value, int):
        raise TypeError("ms_value must be of type int")

    converted_value = datetime.fromtimestamp(ms_value)
    converted_value = converted_value.strftime("%Y-%m-%d %H:%M:%S")
    converted_value = parse_datetime(converted_value)
    converted_value.replace(tzinfo=zoneinfo.ZoneInfo("Asia/Dubai"))
    return converted_value












# def transposeKeyListForSerializer(category_list: list, key: str) -> list:

#     if not isinstance(category_list, list):
#         raise TypeError("category_list must be of type list")
#     if not isinstance(key, str):
#         raise TypeError("Key must be a string")
#     if not all(isinstance(elem, str) for elem in category_list):
#         raise TypeError("All elements in category_list must be of type string")

#     transposed_list = []

#     for elem in category_list:
#         transposed_list.append({f"{key}": f"{elem}"})

#     return transposed_list


# def getQueryCategories() -> list:
#     category_list = list(ACCESS_ROUTES.keys())
#     category_list.pop(0)

#     try:
#         formatted_category_list = transposeKeyListForSerializer(category_list, "category")
#     except TypeError as e:
#         return {"error": f"Error: {e}"} 

#     return formatted_category_list


# def getQueryCategoryRoutes(category) -> list:
#     route_list = list(ACCESS_ROUTES[category].keys())

#     return transposeKeyListForSerializer(route_list, "route")


# def processURLAndParamsToList(url, params: dict) -> list:

#     params_string_for_return = ""

#     for key in params.keys():
#         print(key)
#         params_string_for_return += key

#     data_dict = {
#         "url": url["url"],
#         "params": params_string_for_return,
#     }

#     return [data_dict]

# def getAPIParams(category, query) -> dict:
#     return ACCESS_ROUTES[category][query]["params"]





# def getDictOfPossibleFilters() -> dict:
#     return ACCESS_ROUTES["meta"]["filters"]

# def getFilters() -> dict:
#     return ACCESS_ROUTES["meta"]["filters"]