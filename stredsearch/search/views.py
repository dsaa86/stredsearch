from search.models import *
from search.serializers import *
from rest_framework import mixins
from rest_framework import generics
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from .stackquery import *
from .redditquery import *
import html5lib


class GetAllStackOverFlowCategories(APIView):
    def get(self, request):
        category_list = getQueryCategories()

        results = StackCategoriesSerializer(category_list, many=True).data

        return Response(results)


class GetStackOverflowRoutesFromCategory(APIView):
    def get(self, request, category):
        route_list = getQueryCategoryRoutes(category)
        print(route_list)

        results = StackRoutesSerializer(route_list, many=True).data

        return Response(results)


class GetStackOverflowRouteURLAndParams(APIView):
    def get(self, request, category, route):
        url = getAPIRoute(category, route)
        params = getAPIParams(category, route)

        url_and_params = processURLAndParamsToList(url, params)

        results = StackRoutesURLAndParamsSerializer(url_and_params, many=True).data

        return Response(results)


class GetStackoverflowData(APIView):
    def processResultsForSerialization(results: dict) -> dict:
        pass

    def removeBlankParams(self, keys_to_delete: list, params_dict: dict) -> dict:
        for key in keys_to_delete:
            del params_dict[key]

        return params_dict

    def processFilters(self, params_dict: dict) -> dict:
        keys_to_delete = []
        for key, value in params_dict.items():
            if value == " ":
                keys_to_delete.append(key)

            if key == "tagged":
                params_dict[key] = value.replace(",", ";")

        params_dict = self.removeBlankParams(keys_to_delete, params_dict)

        return params_dict

    def get(
        self,
        request,
        category,
        query,
        page,
        pagesize,
        fromdate,
        todate,
        order,
        min,
        max,
        sort,
        tagged,
        format=None,
    ):
        params_dict = {
            "page": page,
            "pagesize": pagesize,
            "fromdate": fromdate,
            "todate": todate,
            "order": order,
            "min": min,
            "max": max,
            "sort": sort,
            "tagged": tagged,
        }

        processed_filters = self.processFilters(params_dict)

        total_search_result_set = queryStackOverflow(category, query, processed_filters)

        # print(total_search_result_set)

        # processed_results = self.processResultsForSerialization(results)

        for elem in total_search_result_set:
            if "user_id" not in elem.keys():
                print(elem)

        results = StackSearchQuerySerializer(total_search_result_set, many=True).data

        return Response(results)


class GetRedditData(APIView):
    def getRedditTerms(self, terms: dict, subred) -> list:
        return searchRedditAndReturnResponse(terms, subred)

    def buildTermsFromParams(self, q: str, type: str, limit: str) -> dict:
        terms = {
            "q": f"{q}",
            "type": f"{type}",
            "limit": f"{limit}",
        }

        return terms

    def parseRedditSearchResults(self, search_results: dict) -> list:
        formatted_results_set = []

        for tuple in search_results:
            result = {"title": f"{tuple[0]}", "link": f"https://reddit.com{tuple[1]},"}

            formatted_results_set.append(result)

        return formatted_results_set

    def buildSubredFromParams(self, subreds):
        return subreds.split(",")

    def get(self, request, subred, q, type, limit, format=None):
        # PARAMS STRUCTURE

        # terms = {
        #     'q' : 'exception raised during for loop python',
        #     'type' : '{ sr | link | user } --> AND = comma delimited',
        #     'limit' : '100'
        # }

        # subred = '/r/{subredname}'

        search_terms = self.buildTermsFromParams(q, type, limit)

        subred_list = self.buildSubredFromParams(subred)

        total_search_result_set = []

        for elem in subred_list:
            reddit_search_results = self.getRedditTerms(search_terms, "/r/" + subred)
            total_search_result_set = (
                total_search_result_set
                + self.parseRedditSearchResults(reddit_search_results)
            )

        results = RedditSearchQuerySerializer(total_search_result_set, many=True).data

        return Response(results)


class QuestionList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = StackQuestion.objects.all()
    serializer_class = StackQuestionSerializer

    def get(self, request, *args, **kwargs):
        terms = {
            "q": "exception raised during for loop python",
            "type": "link",
            "limit": "100",
        }

        subred = "/r/python"
        returned_terms = searchRedditAndReturnResponse(terms, subred)
        print(returned_terms)

        response = queryStackOverflow(
            "questions", "question_by_tag", {"tagged": "python;java"}
        )
        return self.list(request, *args, **kwargs)
