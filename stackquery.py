import requests

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


ACCESS_ROUTES = {
    "meta" : {
        "route_prepend" : "api.stackexchange.com",
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
    print(type(ACCESS_ROUTES['meta']['route_prepend']))
    return ACCESS_ROUTES['meta']['route_prepend']

def getRouteAppend() -> dict:
    return ACCESS_ROUTES['meta']['route_append']

def getFilters() -> dict:
    return ACCESS_ROUTES['meta']['filters']

def queryStackOverflow(category, query, params):
    pass

print(getRoutePrepend())