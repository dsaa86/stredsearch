from multiprocessing import Value, process
from re import A
from urllib.error import HTTPError

import django_rq
import html5lib
import requests
from django.contrib.auth.models import User
from django.http import *
from rest_framework import filters, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from search.databaseinitialisation import DatabaseInitialisation
from search.helperfunctions import processFilters
from search.models import *
from search.redditquery import *
from search.serializers import *
from search.stackquery import getTagsFromSO, queryStackOverflow
from search.tasks import (
    insertRedditQuestionToDB,
    insertSearchToUserProfile,
    insertStackQuestionsToDB,
    insertStackTagsToDB,
)


class RetrieveSearchResults(APIView):
    def get(self, request, token, term):
        user = User.objects.get(auth_token=token)
        try:
            search_history = UserSearchResponses.objects.filter(
                user=user, search_term__search_term=term
            )
        except UserSearchResponses.DoesNotExist:
            raise Http404("No search history found")
        results = RetrieveSearchResultsSerializer(search_history, many=True)
        return Response(results.data)


class SearchHistoryView(APIView):
    def get(self, request, token):
        user = User.objects.get(auth_token=token)
        search_history = UserSearchResponses.objects.filter(user=user)
        results = UserSearchResponsesSerializer(search_history, many=True)
        return Response(results.data)


class UserDetailView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RegisterUserView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            errors = serializer.errors
            if ("email" in errors) or ("username" in errors):
                return Response(errors, status=status.HTTP_409_CONFLICT)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class GetStackOverflowQuestionsByTag(APIView):
    def checkObjAndRaiseTypeError(self, test_obj: object, test_type, error_msg: str):
        if not isinstance(test_obj, test_type):
            raise TypeError(error_msg)
        else:
            return True

    def get(
        self,
        request,
        page,
        pagesize,
        fromdate,
        todate,
        order,
        sort,
        tags,
        token,
        format=None,
    ):
        for elem in [page, pagesize, fromdate, todate, order, sort, tags, token]:
            try:
                self.checkObjAndRaiseTypeError(elem, str, "Invalid type for parameter")
            except TypeError:
                raise Http404("Invalid type for parameter")

        params_dict = {
            "page": page,
            "pagesize": pagesize,
            "fromdate": fromdate,
            "todate": todate,
            "order": order,
            "sort": sort,
            "tagged": tags,
        }

        try:
            processed_filters = processFilters(params_dict)
        except ValueError:
            raise Http404("Invalid value for parameter")

        total_search_result_set = queryStackOverflow(
            "questions", "question_by_tag", processed_filters
        )
        task_queue = django_rq.get_queue("default", autocommit=True, is_async=True)
        task_queue.enqueue(insertStackQuestionsToDB, total_search_result_set)
        if token != " ":
            # enqueue task to commit search to db for user
            task_queue.enqueue(
                insertSearchToUserProfile, token, tags, total_search_result_set, {}
            )

        if (
            type(total_search_result_set) == dict
            and "error" in total_search_result_set.keys()
        ):
            # results = StackSearchErrorSerializer(total_search_result_set).data
            raise HTTPError("No results found")
        else:
            results = StackSearchQuerySerializer(
                total_search_result_set, many=True
            ).data

        return Response(results)


class GetStackOverflowRelatedQuestions(APIView):
    def checkObjAndRaiseTypeError(self, test_obj: object, test_type, error_msg: str):
        if not isinstance(test_obj, test_type):
            raise TypeError(error_msg)
        else:
            return True

    def checkStrAndRaiseValueError(
        self, test_str: str, test_values: list, error_msg: str
    ):
        if test_str in test_values:
            raise ValueError(error_msg)
        else:
            return True

    def get(
        self,
        request,
        page,
        pagesize,
        fromdate,
        todate,
        order,
        sort,
        ids,
        token,
        format=None,
    ):
        for elem in [page, pagesize, fromdate, todate, order, sort, ids]:
            try:
                self.checkObjAndRaiseTypeError(elem, str, "Invalid type for parameter")
                self.checkStrAndRaiseValueError(
                    elem, ["invalid", "err", "error"], "Invalid value for parameter"
                )
            except TypeError as e:
                raise Http404("Invalid type for parameter") from e
            except ValueError as e:
                raise Http404("Invalid value for parameter") from e

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

        total_search_result_set = queryStackOverflow(
            "questions", "related_questions", processed_filters
        )

        task_queue = django_rq.get_queue("default", autocommit=True, is_async=True)
        task_queue.enqueue(insertStackQuestionsToDB, total_search_result_set)
        if token != " ":
            # enqueue task to commit search to db for user
            task_queue.enqueue(
                insertSearchToUserProfile, token, ids, total_search_result_set, {}
            )

        if (
            type(total_search_result_set) == dict
            and "error" in total_search_result_set.keys()
        ):
            results = StackSearchErrorSerializer(total_search_result_set).data
        else:
            results = StackSearchQuerySerializer(
                total_search_result_set, many=True
            ).data

        return Response(results)


class GetStackOverflowSimpleSearch(APIView):
    def checkObjAndRaiseTypeError(self, test_obj: object, test_type, error_msg: str):
        if not isinstance(test_obj, test_type):
            raise TypeError(error_msg)
        else:
            return True

    def checkStrAndRaiseValueError(
        self, test_str: str, test_values: list, error_msg: str
    ):
        if test_str in test_values:
            raise ValueError(error_msg)
        else:
            return True

    def get(
        self,
        request,
        page,
        pagesize,
        fromdate,
        todate,
        order,
        sort,
        nottagged,
        tagged,
        intitle,
        token,
        format=None,
    ):
        for elem in [
            page,
            pagesize,
            fromdate,
            todate,
            order,
            sort,
            nottagged,
            tagged,
            intitle,
        ]:
            try:
                self.checkObjAndRaiseTypeError(elem, str, "Invalid type for parameter")
            except TypeError as e:
                raise Http404("Invalid type for parameter") from e

        # not testing nottagged, tagged, or in title as these could feasibly be the prohibited values
        for elem in [page, pagesize, fromdate, todate, order, sort]:
            try:
                self.checkStrAndRaiseValueError(
                    elem, ["invalid", "err", "error"], "Invalid value for parameter"
                )
            except ValueError as e:
                raise Http404("Invalid value for parameter") from e

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

        total_search_result_set = queryStackOverflow(
            "search", "search", processed_filters
        )

        task_queue = django_rq.get_queue("default", autocommit=True, is_async=True)
        task_queue.enqueue(insertStackQuestionsToDB, total_search_result_set)
        if token != " ":
            # enqueue task to commit search to db for user
            task_queue.enqueue(
                insertSearchToUserProfile, token, tagged, total_search_result_set, {}
            )

        if (
            type(total_search_result_set) == dict
            and "error" in total_search_result_set.keys()
        ):
            results = StackSearchErrorSerializer(total_search_result_set).data
        else:
            results = StackSearchQuerySerializer(
                total_search_result_set, many=True
            ).data

        return Response(results)


class GetStackOverflowAdvancedSearch(APIView):
    def checkObjAndRaiseTypeError(self, test_obj: object, test_type, error_msg: str):
        if not isinstance(test_obj, test_type):
            raise TypeError(error_msg)
        else:
            return True

    def checkStrAndRaiseValueError(
        self, test_str: str, test_values: list, error_msg: str
    ):
        if test_str in test_values:
            raise ValueError(error_msg)
        else:
            return True

    def get(
        self,
        request,
        page,
        pagesize,
        fromdate,
        todate,
        order,
        sort,
        q,
        accepted,
        answers,
        body,
        closed,
        migrated,
        notice,
        nottagged,
        tagged,
        title,
        user,
        url,
        views,
        wiki,
        token,
        format=None,
    ):
        for elem in [
            page,
            pagesize,
            fromdate,
            todate,
            order,
            sort,
            q,
            accepted,
            answers,
            body,
            closed,
            migrated,
            notice,
            nottagged,
            tagged,
            title,
            user,
            url,
            views,
            wiki,
        ]:
            try:
                self.checkObjAndRaiseTypeError(elem, str, "Invalid type for parameter")
            except TypeError as e:
                raise Http404("Invalid type for parameter") from e

        # not testing nottagged, tagged, or in title as these could feasibly be the prohibited values
        for elem in [
            page,
            pagesize,
            fromdate,
            todate,
            order,
            sort,
            accepted,
            answers,
            body,
            closed,
            migrated,
            notice,
            user,
            views,
            wiki,
        ]:
            try:
                self.checkStrAndRaiseValueError(
                    elem, ["invalid", "err", "error"], "Invalid value for parameter"
                )
            except ValueError as e:
                raise Http404("Invalid value for parameter") from e

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

        total_search_result_set = queryStackOverflow(
            "search", "advanced-search", processed_filters
        )

        for result in total_search_result_set:
            if type(result) == dict:
                result["q"] = q

        task_queue = django_rq.get_queue("default", autocommit=True, is_async=True)
        task_queue.enqueue(insertStackQuestionsToDB, total_search_result_set)
        if token != " ":
            # enqueue task to commit search to db for user
            task_queue.enqueue(
                insertSearchToUserProfile, token, q, total_search_result_set, {}
            )

        if (
            type(total_search_result_set) == dict
            and "error" in total_search_result_set.keys()
        ):
            results = StackSearchErrorSerializer(total_search_result_set).data
        else:
            results = StackSearchQuerySerializer(
                total_search_result_set, many=True
            ).data

        return Response(results)


class GetStackOverflowAllTagsInDB(APIView):
    def get(self, request):
        tags = StackTags.objects.all()
        results = StackTagsSerializer(tags, many=True).data
        return Response(results)


class GetStackOverflowTagsFromSite(APIView):
    def get(self, request, pages):
        total_tag_result_set = getTagsFromSO(pages)
        task_queue = django_rq.get_queue("default", autocommit=True, is_async=True)
        task_queue.enqueue(insertStackTagsToDB, total_tag_result_set)

        results = StackTagsSerializer(total_tag_result_set, many=True).data

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
    def get(self, request):
        question_data_fields = StackQuestionDataFields.objects.all()
        results = StackQuestionDataFieldsSerializer(
            question_data_fields, many=True
        ).data
        return Response(results)


class InitialiseDatabase(APIView):
    def get(self, request):
        self.dbinit = DatabaseInitialisation()
        if self.dbinit.initialiseDatabase():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetRedditData(APIView):
    def get(self, request, subred, q, search_type, limit, token, format=None):
        # PARAMS STRUCTURE
        # terms = {
        #     'q' : 'exception raised during for loop python',
        #     'type' : '{ sr | link | user } --> AND = comma delimited',
        #     'limit' : '100'
        # }

        # SR = SubReddit
        # LINK = Post / Thread
        # USER = User account

        # subred = '/r/{subredname}'

        total_search_result_set = searchRedditAndReturnResponse(
            q, search_type, limit, subred
        )

        task_data_set = {
            "search_term": q,
            "search_type_set": search_type,
            "question_set": total_search_result_set,
            "subreddits": subred,
        }
        task_queue = django_rq.get_queue("default", autocommit=True, is_async=True)
        task_queue.enqueue(insertRedditQuestionToDB, task_data_set)
        if token != " ":
            # enqueue task to commit search to db for user
            task_queue.enqueue(
                insertSearchToUserProfile, token, q, {}, total_search_result_set
            )

        results = RedditSearchQuerySerializer(total_search_result_set, many=True).data

        return Response(results)


class StackSearchResponseView(APIView):
    def get(self, request, term):
        print(term)
        # search_history = StackQuestion.objects.filter(title__icontains=term)
        # results = StackSearchQuerySerializer(search_history, many=True).data
        # return Response(results)


class RedditSearchResponseView(APIView):
    def get(self, request, term):
        print(term)
        # search_history = RedditQuestion.objects.filter(title__icontains=term)
        # results = RedditSearchQuerySerializer(search_history, many=True).data
        # return Response(results)


# class StackSearchResponseView(generics.ListCreateAPIView):
#     search_fields = ["title", "tags__tag_name"]
#     filter_backends = (filters.SearchFilter,)
#     queryset = StackQuestion.objects.all()
#     serializer_class = StackSearchQuerySerializer


# class RedditSearchResponseView(generics.ListCreateAPIView):
#     search_fields = ["title", "subreddit__subreddit_name"]
#     filter_backends = (filters.SearchFilter,)
#     queryset = RedditQuestion.objects.all()
#     serializer_class = RedditSearchQuerySerializerForFiltering
