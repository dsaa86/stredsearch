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

class GetStackoverflowData(APIView):
    def get(self, request, route, page, pagesize, fromdate, todate, order, min, max, sort, tagged, format=None):
        pass


class GetRedditData(APIView):
    def getRedditTerms(self, terms: dict, subred) -> list:
        return searchRedditAndReturnResponse(terms, subred)
    
    def buildTermsFromParams(self, q: str, type: str, limit: str) -> dict:
        terms = {
            'q' : f'{q}',
            'type' : f'{type}',
            'limit' : f'{limit}',
        }
    
        return terms
    
    def parseRedditSearchResults(self, search_results: dict) -> list:
        formatted_results_set = []

        for tuple in search_results:
            result = {
                "title" : f"{tuple[0]}",
                "link" : f"https://reddit.com{tuple[1]},"
            }

            formatted_results_set.append(result)

        return formatted_results_set
    
    def buildSubredFromParams(self, subreds):
        return subreds.split(',')
    
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
            reddit_search_results = self.getRedditTerms(search_terms, '/r/'+subred)
            total_search_result_set = total_search_result_set + self.parseRedditSearchResults(reddit_search_results)

        results = RedditSearchQuerySerializer(total_search_result_set, many=True).data

        return Response(results)



class QuestionList(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = StackQuestion.objects.all()
    serializer_class = StackQuestionSerializer

    def get(self, request, *args, **kwargs): 
        terms = {
            'q' : 'exception raised during for loop python',
            'type' : 'link',
            'limit' : '100'
        }

        subred = '/r/python'
        returned_terms = searchRedditAndReturnResponse(terms, subred)
        print(returned_terms)
        
        response = queryStackOverflow('questions', 'question_by_tag', {'tagged' : 'python;java'})
        print(response)
        return self.list(request, *args, **kwargs)

