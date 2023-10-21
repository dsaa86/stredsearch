import requests, json
from datetime import datetime

# params = {
#     "client_id" : "27411",
#     "client_secret" : "Ytvd5*Gmt8e0s1uIOK7slw((",
#     "code" : "J2hKGBSiHNxqiLRcooJVmA))",
#     "redirect_uri" : "https://github.com"
# }

# url = "https://stackoverflow.com/oauth/access_token"

# x = requests.post(url, data=params)

# print(x.content)
# print(x.url)

# ACCESS TOKEN = nlyaZ4k0mlpD6ythDJuEGw))

# pp = pprint.PrettyPrinter(width=150, compact=True)


ACCESS_ROUTES = {
    "meta": {
        "route_prepend": "https://api.stackexchange.com",
        "route_append": {
            "site": "stackoverflow",
        },
        "filters": {
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
        },
    },
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


def transposeKeyListForSerializer(category_list, key):
    for index, elem in enumerate(category_list):
        category_list[index] = {f"{key}": f"{elem}"}

    return category_list


def getQueryCategories() -> list:
    category_list = list(ACCESS_ROUTES.keys())
    category_list.pop(0)

    formatted_category_list = transposeKeyListForSerializer(category_list, "category")

    return formatted_category_list


def getQueryCategoryRoutes(category) -> list:
    route_list = list(ACCESS_ROUTES[category].keys())

    formatted_route_list = transposeKeyListForSerializer(route_list, "route")

    return formatted_route_list


def processURLAndParamsToList(url, params):
    data_list = {}

    data_list["url"] = url["url"]

    params_string_for_return = ""

    print(len(params.keys()))

    for key in params.keys():
        print(key)
        params_string_for_return += key

    data_list["params"] = params_string_for_return

    processed_data = []
    processed_data.append(data_list)

    return processed_data


def getAPIRoute(category, query) -> str:
    api_route = ACCESS_ROUTES[category][query]["route"]

    formatted_api_route = {"url": f"{api_route}"}
    return formatted_api_route


def getAPIParams(category, query) -> dict:
    api_params = ACCESS_ROUTES[category][query]["params"]
    return api_params


def getRoutePrepend() -> str:
    return ACCESS_ROUTES["meta"]["route_prepend"]


def getRouteAppend() -> dict:
    return ACCESS_ROUTES["meta"]["route_append"]


def getDictOfPossibleFilters() -> dict:
    return ACCESS_ROUTES["meta"]["filters"]


def getQuestionsOnlyFromStackOverflowResponse(json_response: json) -> dict:
    return json_response["items"]


def convertListToString(list_to_convert: list, delimiter: str = None) -> str:
    return_string = ""
    for index, value in enumerate(list_to_convert):
        return_string += str(value)
        if delimiter != None and index + 1 != len(list_to_convert):
            return_string += f"{delimiter} "

    return return_string


def convertMSToDateTime(ms_value: int) -> object:
    converted_value = datetime.fromtimestamp(ms_value)
    return converted_value


def sanitiseStackOverflowResponse(json_response):
    # full data set contains additional meta data that is unnecessary. This call strips away that meta data.
    complete_question_set = getQuestionsOnlyFromStackOverflowResponse(json_response)

    sanitised_data = []

    for question in complete_question_set:
        question_data = {}

        question_data["tags"] = convertListToString(question["tags"], ",")

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
            if (
                key == "last_activity_date"
                or key == "creation_date"
                or key == "last_edit_date"
            ):
                question_data[key] = convertMSToDateTime(question_data[key])

        sanitised_data.append(question_data)

    return sanitised_data


def queryStackOverflow(category, query, filters) -> dict:
    url = getRoutePrepend() + getAPIRoute(category, query)
    params = filters

    params["site"] = getRouteAppend()["site"]

    try:
        query_response = requests.get(url, params)
    # Error raised typically when there is no internet connection on the client device
    except requests.exceptions.SSLError as e:
        return {"error": f"Error: Requests SSLError, {e.strerror}"}

    json_response = json.loads(query_response.content)

    sanitised_data_for_return = sanitiseStackOverflowResponse(json_response)

    for data in sanitised_data_for_return:
        print(data)
        print()
        print()

    return sanitised_data_for_return
