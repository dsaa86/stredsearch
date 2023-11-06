import json
from typing import Union

import requests
from search.exceptionhandlers import InvalidDisplayNameKey, InvalidUserIdKey
from search.helperfunctions import convertListToString, convertMSToDateTime
from search.models import StackQuestionDataFields, StackRoute, StackRouteMeta


# MyPy is installed and has been run against this code - technically error checking in this way is unnecessary. As this isn't performance-optimised code, it doesn't hurt to include a belt-and-braces check.
def checkObjAndRaiseTypeError(test_obj: object, test_type, error_msg: str):
    if not isinstance(test_obj, test_type):
        raise TypeError(error_msg)
    else:
        return True


def checkStringAndRaiseValueError(test_string: str, test_value: str, error_msg: str):
    if test_string == test_value:
        raise ValueError(error_msg)
    else:
        return True
    
def checkElemExistsInListOrDict(elem: str, list_or_dict: Union[list, dict], error_msg: str):
    if elem not in list_or_dict:
        raise ValueError(error_msg)
    else:
        return True


def queryStackOverflow(category:str, query:str, filters:dict) -> dict:

    checkObjAndRaiseTypeError(category, str, "category must be of type str")
    checkObjAndRaiseTypeError(query, str, "query must be of type str")
    checkObjAndRaiseTypeError(filters, dict, "filters must be of type dict")


    # removes leading and trailing whitespace...means only one ValueError check needs to be performed that covers both "" and " "
    category = category.strip(' ')
    query = query.strip(' ')
    checkStringAndRaiseValueError(category, '', "category must not be empty string")
    checkStringAndRaiseValueError(query, '', "query must not be empty string")

    route_prepend = getRoutePrepend()
    query_route = getAPIRoute(category, query)

    if query == "related_questions":
        query_route = insertQuestionIdsToQueryRoute(query_route, filters["ids"])
        del filters["ids"]

    url = route_prepend + query_route
    # url = "https://api.stackexchange.com/2.3/questions"
    params = filters
    params["site"] = getRouteAppend()
    # params["site"] = "stackoverflow"

    # An unconventional way of handling errors, but it ensures that the Django view always receives a dict response - this can then be parsed to decide if the response is an error or a valid set of SO data.
    try:
        query_response = requests.get(url, params)
    # SSLError raised typically when there is no internet connection on the client device
    except requests.exceptions.SSLError as e:
        return { "Error": { "SSLError": f"{ e }" } }
    except requests.exceptions.Timeout as e:
        return { "Error": { "Timeout": f"{ e }" } }
    except requests.exceptions.ConnectionError as e:
        return { "Error": { "ConnectionError": f"{ e }" } }
    except requests.exceptions.HTTPError as e:
        return { "Error": { "HTTPError": f"{ e }" } }
    except requests.exceptions.TooManyRedirects as e:
        return { "Error": { "TooManyRedirects": f"{ e }" } }
    except requests.exceptions.RequestException as e:
        return { "Error": { "RequestException": f"{ e }" } }

    json_response = json.loads(query_response.content)

    return sanitiseStackOverflowResponse(json_response)


def getRoutePrepend() -> str:
    prepend = StackRouteMeta.objects.get(pk=1)
    return prepend.route_prepend


def getAPIRoute(category:str, query:str) -> str:

    checkObjAndRaiseTypeError(category, str, "category must be of type str")
    checkObjAndRaiseTypeError(query, str, "query must be of type str")

    category = category.strip(' ')
    query = query.strip(' ')
    checkStringAndRaiseValueError(category, '', "category must not be empty string")
    checkStringAndRaiseValueError(query, '', "query must not be empty string")

    return StackRoute.objects.filter(route_category=category, route_query=query).first().route


def insertQuestionIdsToQueryRoute(query_route: str, ids: str) -> str:

    checkObjAndRaiseTypeError(query_route, str, "query_route must be of type str")
    checkObjAndRaiseTypeError(ids, str, "ids must be of type str")

    query_route = query_route.strip(' ')
    ids = ids.strip(' ')
    checkStringAndRaiseValueError(query_route, '', "query_route must not be empty string")
    checkStringAndRaiseValueError(ids, '', "ids must not be empty string")

    return query_route.replace("{question_ids}", ids)

def getRouteAppend() -> str:
    append = StackRouteMeta.objects.get(pk=1)
    return append.route_append


def sanitiseStackOverflowResponse(json_response):

    checkObjAndRaiseTypeError(json_response, dict, "json_response must be of type dict")

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


def getOnlyQuestionsFromStackOverflowResponse(json_response: dict) -> dict:

    checkObjAndRaiseTypeError(json_response, dict, "json_response must be of type dict")
    checkElemExistsInListOrDict("items", json_response.keys(), "json_response must contain a key named 'items'")

    if not json_response["items"]:
        raise ValueError("json_response must contain a non-empty 'items' key")

    return json_response["items"]


def getQuestionData(question:dict) -> dict:

    checkObjAndRaiseTypeError(question, dict, "question must be of type dict")
    checkElemExistsInListOrDict("tags", question.keys(), "question must contain a key named 'tags'")
    checkElemExistsInListOrDict("owner", question.keys(), "question must contain a key named 'owner'")
    checkObjAndRaiseTypeError(question["tags"], list, "question['tags'] must be of type list")
    checkObjAndRaiseTypeError(question["owner"], dict, "question['owner'] must be of type dict")

    question_data = {}

    try:
        question_data['tags'] = convertListToString(question["tags"], ",")
    except TypeError as e:
        return {"error": f"Error: {e}"}
    
    try:
        question_data["user_id"] = extractOwnerData(question, "user_id")
    except TypeError as e:
        return { "error": { "TypeError": f"{ e }" } } 
    except ValueError as e:
        return { "error": { "ValueError": f"{  e }" } }
    except InvalidUserIdKey as e:
        # Sometimes there isn't a user due to user account being deleted on SO - we don't want the programme to crash, which it would if handled as a typical KeyError.
        pass
    except KeyError as e:
        return { "error": { "KeyError": f"{ e }" } }
    try:
        question_data["display_name"] = extractOwnerData(question, "display_name")
    except TypeError as e:
        return { "error": { "TypeError": f"{ e }" } } 
    except ValueError as e:
        return { "error": { "ValueError": f"{  e }" } }
    except InvalidDisplayNameKey as e:
        # Sometimes there isn't a user due to user account being deleted on SO - we don't want the programme to crash, which it would if handled as a typical KeyError.
        pass
    except KeyError as e:
        return { "error": { "KeyError": f"{ e }" } }

    # Individual questions are not forced to have all fields present,
    # this logic prevents fields that aren't present in a question from
    # being appended as empty or raising an exception during runtime
    question_data_fields_for_question = extractRelevantQuestionDataFieldsForQuestion(question)
    question_data |= question_data_fields_for_question

    return question_data


def extractOwnerData(question: dict, key: str) -> str:

    checkObjAndRaiseTypeError(question, dict, "question must be of type dict")
    checkObjAndRaiseTypeError(key, str, "key must be of type str")
    checkElemExistsInListOrDict("owner", question.keys(), "question must contain a key named 'owner'")
    checkObjAndRaiseTypeError(question["owner"], dict, "question['owner'] must be of type dict")

    if key not in question["owner"].keys() and key == "user_id":
        raise InvalidUserIdKey()
    if key not in question["owner"].keys() and key == "display_name":
        raise InvalidDisplayNameKey()
    if key == 'user_id' and not isinstance(question["owner"][key], int):
        raise TypeError(f"question['owner']['{key}'] must be of type int")
    if key == 'display_name' and not isinstance(question["owner"][key], str):
        raise TypeError(f"question['owner']['{key}'] must be of type str")
    
    checkElemExistsInListOrDict(key, ["user_id", "display_name"], "key must be one of the following: 'user_id', 'display_name'")

    for owner_data_key, owner_data_value in question["owner"].items():
        if owner_data_key == "user_id" and key == "user_id":
            return owner_data_value
        if owner_data_key == "display_name" and key == "display_name":
            return owner_data_value
        

def extractRelevantQuestionDataFieldsForQuestion(question: dict) -> dict:

    checkObjAndRaiseTypeError(question, dict, "question must be of type dict")

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
                return {"error": { "TypeError" : f"{ e }" } }
    return matched_data_fields


def getQuestionDataFields() -> list:
    data_fields_from_db = StackQuestionDataFields.objects.all()
    return [field.data_field_name for field in data_fields_from_db]


def getTagsFromSO(pages:int) -> list:

    checkObjAndRaiseTypeError(pages, int, "pages must be of type int")

    route_prepend = getRoutePrepend()

    url = f"{route_prepend}/2.3/tags"
    tags = []
    for count in range(0,pages):
        params = {
            "page": count+1,
            "pagesize": 100,
            "site": getRouteAppend()
        }

        try:
            query_response = requests.get(url, params)
        # SSLError raised typically when there is no internet connection on the client device
        except requests.exceptions.SSLError as e:
            return { "Error": { "SSLError": f"{ e }" } }
        except requests.exceptions.Timeout as e:
            return { "Error": { "Timeout": f"{ e }" } }
        except requests.exceptions.ConnectionError as e:
            return { "Error": { "ConnectionError": f"{ e }" } }
        except requests.exceptions.HTTPError as e:
            return { "Error": { "HTTPError": f"{ e }" } }
        except requests.exceptions.TooManyRedirects as e:
            return { "Error": { "TooManyRedirects": f"{ e }" } }
        except requests.exceptions.RequestException as e:
            return { "Error": { "RequestException": f"{ e }" } }

        json_response = json.loads(query_response.content)

        try:
            item_data = json_response["items"]
        except Exception as e:
            return { "error" : f"Error in SO response {e}"}

        for item in item_data:
            tags.append({"tag_name" : item["name"], "number_of_instances_on_so" : item["count"]})
    return tags