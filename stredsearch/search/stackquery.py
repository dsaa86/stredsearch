import json

import requests
from search.exceptionhandlers import InvalidDisplayNameKey, InvalidUserIdKey
from search.helperfunctions import convertListToString, convertMSToDateTime
from search.models import StackQuestionDataFields, StackRoute, StackRouteMeta


def queryStackOverflow(category, query, filters) -> dict:
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

    try:
        query_response = requests.get(url, params)
        print(query_response)
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


def getAPIRoute(category, query) -> str:
    return StackRoute.objects.filter(route_category=category, route_query=query).first().route


def insertQuestionIdsToQueryRoute(query_route: str, ids: str) -> str:
    if not isinstance(query_route, str):
        raise TypeError("query_route must be of type str")
    if not isinstance(ids, str):
        raise TypeError("ids must be of type str")

    return query_route.replace("{question_ids}", ids)

def getRouteAppend() -> str:
    append = StackRouteMeta.objects.get(pk=1)
    return append.route_append


def sanitiseStackOverflowResponse(json_response):

    if not isinstance(json_response, dict):
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


def getOnlyQuestionsFromStackOverflowResponse(json_response: dict) -> dict:

    if not isinstance(json_response, dict):
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

    if not isinstance(question, dict):
        raise TypeError("question must be of type dict")
    if not isinstance(key, str):
        raise TypeError("key must be of type str")
    if "owner" not in question.keys():
        raise KeyError("question must contain a key named 'owner'")
    if not isinstance(question["owner"], dict):
        raise TypeError("question['owner'] must be of type dict")
    if key not in question["owner"].keys() and key == "user_id":
        raise InvalidUserIdKey()
    if key not in question["owner"].keys() and key == "display_name":
        raise InvalidDisplayNameKey()
    if key == 'user_id' and not isinstance(question["owner"][key], int):
        raise TypeError(f"question['owner']['{key}'] must be of type int")
    if key == 'display_name' and not isinstance(question["owner"][key], str):
        raise TypeError(f"question['owner']['{key}'] must be of type str")
    if key not in ["user_id", "display_name"]:
        raise ValueError("key must be one of the following: 'user_id', 'display_name'")

    for owner_data_key, owner_data_value in question["owner"].items():
        if owner_data_key == "user_id" and key == "user_id":
            return owner_data_value
        if owner_data_key == "display_name" and key == "display_name":
            return owner_data_value
        

def extractRelevantQuestionDataFieldsForQuestion(question: dict) -> dict:

    if not isinstance(question, dict):
        raise TypeError("question must be of type dict")

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