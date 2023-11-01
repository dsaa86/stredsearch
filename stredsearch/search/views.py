from multiprocessing import process

import django_rq
import html5lib
import requests
from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from search.databaseinitialisation import DatabaseInitialisation
from search.helperfunctions import processFilters
from search.models import *
# from search.redditquery import *
from search.serializers import *
from search.stackquery import queryStackOverflow
from search.tasks import insertStackQuestionsToDB


class GetStackOverflowQuestionsByTag(APIView):

    def get(self, request, page, pagesize, fromdate, todate, order, sort, tags, format=None):

        params_dict = {
            "page": page,
            "pagesize": pagesize,
            "fromdate": fromdate,
            "todate": todate,
            "order": order,
            "sort": sort,
            "tagged": tags,
        }

        processed_filters = processFilters(params_dict)

        total_search_result_set = queryStackOverflow("questions", "question_by_tag", processed_filters)
        print(total_search_result_set)
        task_queue = django_rq.get_queue("default", autocommit=True, is_async=True)
        task_queue.enqueue(insertStackQuestionsToDB, total_search_result_set)

        if type(total_search_result_set) == dict and "error" in total_search_result_set.keys():
            results = StackSearchErrorSerializer(total_search_result_set).data
        else:
            results = StackSearchQuerySerializer(total_search_result_set, many=True).data

        return Response(results)

        

class GetStackOverflowRelatedQuestions(APIView):

    def get(self, request, page, pagesize, fromdate, todate, order, sort, ids, format=None):
        
        params_dict = {
            "page": page,
            "pagesize": pagesize,
            "fromdate": fromdate,
            "todate": todate,
            "order": order,
            "sort": sort,
            "ids": ids,
        }

        processed_filters = processFilters(params_dict)

        total_search_result_set = queryStackOverflow("questions", "related_questions", processed_filters)

        if type(total_search_result_set) == dict and "error" in total_search_result_set.keys():
            results = StackSearchErrorSerializer(total_search_result_set).data
        else:
            results = StackSearchQuerySerializer(total_search_result_set, many=True).data

        return Response(results)

class GetStackOverflowSimpleSearch(APIView):
    def get(self, request, page, pagesize, fromdate, todate, order, min, max, sort, nottagged, tagged, intitle, format=None):
        
        params_dict = {
            "page": page,
            "pagesize": pagesize,
            "fromdate": fromdate,
            "todate": todate,
            "order": order,
            "sort": sort,
            "nottagged": nottagged,
            "tagged": tagged,
            "intitle": intitle,
        }

        processed_filters = processFilters(params_dict)

        total_search_result_set = queryStackOverflow("search", "search", processed_filters)

        if type(total_search_result_set) == dict and "error" in total_search_result_set.keys():
            results = StackSearchErrorSerializer(total_search_result_set).data
        else:
            results = StackSearchQuerySerializer(total_search_result_set, many=True).data

        return Response(results)

class GetStackOverflowAdvancedSearch(APIView):
    def get(self, request, page, pagesize, fromdate, todate, order, min, max, sort, q, accepted, answers, body, closed, migrated, notice, nottagged, tagged, title, user, url, views, wiki, format=None):
        
        params_dict = {
            "page": page,
            "pagesize": pagesize,
            "fromdate": fromdate,
            "todate": todate,
            "order": order,
            "sort": sort,
            "q": q,
            "accepted": accepted,
            "answers": answers,
            "body": body,
            "closed": closed,
            "migrated": migrated,
            "notice": notice,
            "nottagged": nottagged,
            "tagged": tagged,
            "title": title,
            "user": user,
            "url": url,
            "views": views,
            "wiki": wiki,
        }

        processed_filters = processFilters(params_dict)

        total_search_result_set = queryStackOverflow("search", "advanced-search", processed_filters)

        if type(total_search_result_set) == dict and "error" in total_search_result_set.keys():
            results = StackSearchErrorSerializer(total_search_result_set).data
        else:
            results = StackSearchQuerySerializer(total_search_result_set, many=True).data

        return Response(results)

class GetStackOverflowAllTagsInDB(APIView):
    def get(self, request):
        tags = StackTags.objects.all()
        results = StackTagsSerializer(tags, many=True).data
        return Response(results)

class GetAllStackOverflowParams(APIView):
    def get(self, request):
        params = StackParams.objects.all()
        results = StackParamsSerializer(params, many=True).data
        return Response(results)
    
class GetStackOverflowParams(APIView):
    def get(self, request):
        pass

class GetStackOverflowRoutes(APIView):  
    def get(self, request):
        routes = StackRoute.objects.all()
        results = StackRouteSerializer(routes, many=True).data
        return Response(results)

class GetAllStackOverflowFilters(APIView):
    def get(self, request):
        filters = StackFilters.objects.all()
        results = StackFiltersSerializer(filters, many=True).data
        return Response(results)
    
class GetStackOverflowFilters(APIView):
    def get(self, request):
        pass

class GetStackOverflowSortMethods(APIView):
    def get(self, request):
        sort_methods = StackSortMethods.objects.all()
        results = StackSortMethodsSerializer(sort_methods, many=True).data
        return Response(results)

class GetStackOverflowOrderMethods(APIView):
    def get(self, request):
        order_methods = StackOrderMethods.objects.all()
        results = StackOrderMethodsSerializer(order_methods, many=True).data
        return Response(results)

class GetStackOverflowQuestionDataFields(APIView):
    def get(self,request):
        question_data_fields = StackQuestionDataFields.objects.all()
        results = StackQuestionDataFieldsSerializer(question_data_fields, many=True).data
        return Response(results)


class InitialiseDatabase(APIView):
    def get(self, request):
        self.dbinit = DatabaseInitialisation()
        if self.dbinit.initialiseDatabase():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class GetUserByName(APIView):
#     def get(self, request, display_name):
#         try:
#             users = StackUser.objects.all().filter(display_name=display_name)
#             results = StackUserSerializer(users, many=True).data
#             return Response(results)
#         except Exception as e:
#             raise APIException(e)


# class AddNewUser(APIView):
#     def get(self, request, display_name, user_id):
#         results = StackUserSerializer([{"display_name": display_name, "user_id": user_id}], many=True).data
#         new_user = StackUser.objects.create(display_name=display_name, user_id=user_id)
#         task_queue = django_rq.get_queue("default", autocommit=True, is_async=True)
#         data = {"display_name": display_name, "user_id": user_id}
#         task_queue.enqueue(task_execute, data)
#         # task_execute.delay(name)
#         return Response(results)


# class GetAllStackOverFlowCategories(APIView):
#     def get(self, request):
#         category_list = getQueryCategories()

#         results = StackCategoriesSerializer(category_list, many=True).data

#         return Response(results)


# class GetStackOverflowRoutesFromCategory(APIView):
#     def get(self, request, category):
#         route_list = getQueryCategoryRoutes(category)
#         print(route_list)

#         results = StackRoutesSerializer(route_list, many=True).data

#         return Response(results)


# class GetStackOverflowRouteURLAndParams(APIView):
#     def get(self, request, category, route):
#         url = getAPIRoute(category, route)
#         params = getAPIParams(category, route)

#         url_and_params = processURLAndParamsToList(url, params)

#         results = StackRoutesURLAndParamsSerializer(url_and_params, many=True).data

#         return Response(results)


# class GetStackoverflowData(APIView):
#     def removeBlankParams(self, keys_to_delete: list, params_dict: dict) -> dict:
#         for key in keys_to_delete:
#             del params_dict[key]

#         return params_dict

#     def processFilters(self, params_dict: dict) -> dict:
#         keys_to_delete = []

#         # " " indicates a param not used in this search on the
#         # part of the user.
#         for key, value in params_dict.items():
#             if value == " ":
#                 keys_to_delete.append(key)

#             # Stack Exchange expects semi-colon delimited list
#             if key == "tagged":
#                 params_dict[key] = value.replace(",", ";")

#         params_dict = self.removeBlankParams(keys_to_delete, params_dict)

#         return params_dict

#     def get(self, request, category, query, page, pagesize, fromdate, todate, order, min, max, sort, tagged, format=None):
#         #
#         # LOGIC FOR RETRIEVING STACKOVERFLOW QUESTIONS
#         #
#         # 1.    .processFilters -> Not all filters are required by a
#         #       user. This function breaks apart user-specified
#         #       filters from those that are not specified for this
#         #       particular query.
#         #
#         # 2.    .queryStackOverflow -> Most of the sanitisation for
#         #       the query is performed within the SO search library.
#         #       The necessary data is passed to this function and a
#         #       data set is returned.
#         #
#         # 3.    The results are serialized and passed to the response
#         #

#         # FIXME Need to account for additional params for the advanced search function. | CREATED: 12:42 23/10/2023

#         params_dict = {
#             "page": page,
#             "pagesize": pagesize,
#             "fromdate": fromdate,
#             "todate": todate,
#             "order": order,
#             "min": min,
#             "max": max,
#             "sort": sort,
#             "tagged": tagged,
#         }

#         processed_filters = self.processFilters(params_dict)

#         total_search_result_set = queryStackOverflow(category, query, processed_filters)

#         results = StackSearchQuerySerializer(total_search_result_set, many=True).data

#         # commit_questions_to_local_db_signal.send(
#         #     sender=None, questions=total_search_result_set, search_term=None
#         # )

#         return Response(results)


# class GetRedditData(APIView):
    # TODO This needs refactoring so that the heavy lifting is done within the library and not here. | CREATED: 12:37 23/10/2023
    #
    # LOGIC FLOW FOR RETRIEVING REDDIT QUESTIONS:
    #
    # 1.    .get -> master function controlling request to Reddit
    #       Function receives the subreddites to search, question
    #       data and the type of search that should be performed
    #       (questions/subreds/users)
    #
    # 2.    .buildTermsFromParams -> builds the required dict of
    #       terms that Reddit API expects. This is simply a
    #       formatted version of the provided question and
    #       params that are received from the UI.
    #
    # 3.    .buildSubredFromParams -> Subreds to search are
    #       provided from the UI as a comma-separated string.
    #       This function breaks the string in to a list by
    #       the delimiter.
    #
    # 4.    The list of subreds is iterated and a search of
    #       Reddit is perfomred at each iteration. Reddit API
    #       requires that each subred is searched individually.
    #
    # 5.    .getRedditTerms -> A simple handler function that
    #       initiates the search to Reddit API, passing this
    #       to the appropriate search function in the Reddit
    #       module.
    #
    # 6.    .parseRedditSearchResults -> The Reddit module
    #       returns a dict of tuples. Each tuple contains
    #       two elements - a question title and the link to that
    #       question. Each tuple is iterated and turned in to a
    #       dict, the dict is then appended to a list. The list
    #       of dicts is then returned.
    #
    # 7.    Every set of responses from the individual searches
    #       on the Reddit API is appended to a master list after
    #       being parsed in the last step. This master list is
    #       passed to the serializer and the data response from
    #       this returned as a part of the response.
    #

    # def getRedditTerms(self, terms: dict, subred) -> list:
    #     return searchRedditAndReturnResponse(terms, subred)

    # def buildTermsFromParams(self, q: str, type: str, limit: str) -> dict:
    #     terms = {
    #         "q": f"{q}",
    #         "type": f"{type}",
    #         "limit": f"{limit}",
    #     }

    #     return terms

    # def parseRedditSearchResults(self, search_results: dict) -> list:
    #     formatted_results_set = []

    #     for tuple in search_results:
    #         result = {"title": f"{tuple[0]}", "link": f"https://reddit.com{tuple[1]},"}

    #         formatted_results_set.append(result)

    #     return formatted_results_set

    # def buildSubredFromParams(self, subreds):
    #     return subreds.split(",")

    # def get(self, request, subred, q, type, limit, format=None):
    #     # PARAMS STRUCTURE
    #     # terms = {
    #     #     'q' : 'exception raised during for loop python',
    #     #     'type' : '{ sr | link | user } --> AND = comma delimited',
    #     #     'limit' : '100'
    #     # }

    #     # subred = '/r/{subredname}'

    #     search_terms = self.buildTermsFromParams(q, type, limit)

    #     subred_list = self.buildSubredFromParams(subred)

    #     total_search_result_set = []

    #     for elem in subred_list:
    #         reddit_search_results = self.getRedditTerms(search_terms, "/r/" + subred)
    #         total_search_result_set = (
    #             total_search_result_set
    #             + self.parseRedditSearchResults(reddit_search_results)
    #         )

    #     results = RedditSearchQuerySerializer(total_search_result_set, many=True).data

    #     return Response(results)


# class QuestionList(mixins.ListModelMixin, generics.GenericAPIView):
#     queryset = StackQuestion.objects.all()
#     serializer_class = StackQuestionSerializer

#     def get(self, request, *args, **kwargs):
#         terms = {
#             "q": "exception raised during for loop python",
#             "type": "link",
#             "limit": "100",
#         }

#         subred = "/r/python"
#         returned_terms = searchRedditAndReturnResponse(terms, subred)
#         print(returned_terms)

#         response = queryStackOverflow(
#             "questions", "question_by_tag", {"tagged": "python;java"}
#         )
#         return self.list(request, *args, **kwargs)