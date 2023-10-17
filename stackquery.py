import requests, json

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
    "meta" : {
        "route_prepend" : "https://api.stackexchange.com",
        "route_append" : {
            "site" : "stackoverflow",
        },
        "filters" : {
            "fromdate" : "filter by oldest age of question",
            "todate" : "filter by youngest age of question",
            "min" : "filter by youngest possible age of question",
            "max" : "filter by oldest possible age of question",
            "page" : "the page number of results to show",
            "pagesize" : "the number of results per page (max 100)",
            "order" : {
                "asc" : "order by ascending order",
                "desc" : "order by descending order"
            },
            "sort" : {
                "activity" : "sort by recent activity", 
                "votes" : "sort by number of votes", 
                "creation" : "sort by creation date", 
                "hot" : "sort by current popularity of question", 
                "week" : "sort by creation week", 
                "month" : "sort by creation month",
            }
        },
    },
    "questions" : {
        "question_by_tag" : {
            "route" : "/2.3/questions",
            "params" : {
                "tagged" : "tags that describe the question topic, e.g. 'python'",
            },
        },    
        "related_questions" : {
            "route" : "/2.3/questions/{ids}/linked",
            "params" : {
                "ids" : "the id(s) of questions for which to find other, related questions",
            }
        }
    },
    "search" : {
        "search" : {
            "route" : "/2.3/search",
            "params" : {
               "tagged" : "the tags by which to search for questions",
                "nottagged" : "tags of questions to be omitted from the search",
                "intitle" : "text that should be present in the title of the question",
            }
        },
    },
}

def getQueryCategories() -> list:
    category_list = list(ACCESS_ROUTES.keys())
    category_list.pop(0)

    return category_list

def getQueryCategoryRoutes(category) -> list:
    route_list = list(ACCESS_ROUTES[category].keys())
    return route_list

def getAPIRoute(category, query) -> str:
    api_route = ACCESS_ROUTES[category][query]['route']
    return api_route

def getAPIParams(category, query) -> dict:
    api_params = ACCESS_ROUTES[category][query]['params']
    return api_params

def getRoutePrepend() -> str:
    return ACCESS_ROUTES['meta']['route_prepend']

def getRouteAppend() -> dict:
    return ACCESS_ROUTES['meta']['route_append']

def getDictOfPossibleFilters() -> dict:
    return ACCESS_ROUTES['meta']['filters']

def processUserChosenFilters(filters) -> dict:
    data = {}

    if 'page' in filters and filters['page'] != None:
        data['page'] = filters['page']
    if 'pagesize' in filters and filters['pagesize'] != None:
        data['pagesize'] = filters['pagesize']
    if 'fromdate' in filters and filters['fromdate'] != None:
        data['fromdate'] = filters['fromdate']
    if 'todate' in filters and filters['todate'] != None:
        data['todate'] = filters['todate']
    if 'order' in filters and filters['order'] != None:
        data['order'] = filters['order']
    if 'min' in filters and filters['min'] != None:
        data['min'] = filters['min']
    if 'max' in filters and filters['max'] != None:
        data['max'] = filters['max']
    if 'sort' in filters and filters['sort'] != None:
        data['sort'] = filters['sort']
    if 'tagged' in filters and filters['tagged'] != None:
        data['tagged'] = filters['tagged']

    return data

def sanitise_stack_overflow_response(json_response):

    question_data_to_check = ['is_answered', 'view_count', 'answer_count', 'score', 'last_activity_date', 'creation_date', 'last_edit_date', 'question_id', 'link', 'title']

    sanitised_data = {}

    for question in json_response['items']:

        question_keys = question.keys()
        extracted_data = {}
        extracted_data['tags'] = question['tags']

        owner_details = {
            'user_id' : question['owner']['user_id'],
            'display_name' : question['owner']['display_name'],
        }
        extracted_data['owner'] = owner_details

        question_details = {}

        for question_data in question_data_to_check:
        
            if question_data in question_keys:
                question_details[question_data] = question[question_data]
        
        extracted_data['question'] = question_details

        sanitised_data[question['question_id']] = extracted_data

    return sanitised_data

def queryStackOverflow(category, query, filters) -> dict:

    url = getRoutePrepend() + getAPIRoute(category, query)
    params = processUserChosenFilters(filters)
    params['site'] = getRouteAppend()['site']

    query_response = requests.get(url, params)

    json_response = json.loads(query_response.content)

    sanitised_data_for_commit = sanitise_stack_overflow_response(json_response)

    return sanitised_data_for_commit


# response = queryStackOverflow('questions', 'question_by_tag', {'tagged' : 'python;java'})

# print(response)