from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from search import views

urlpatterns = [
    # Stack Overflow Routes
    # GET data
    path(
        "stack/get/question_by_tag/<str:page>/<str:pagesize>/<str:fromdate>/<str:todate>/<str:order>/<str:sort>/<str:tags>/<str:token>/",
        views.GetStackOverflowQuestionsByTag.as_view(),
        name="GetStackOverflowQuestionsByTag",
    ),
    path(
        "stack/get/related_questions/<str:page>/<str:pagesize>/<str:fromdate>/<str:todate>/<str:order>/<str:sort>/<str:ids>/<str:token>/",
        views.GetStackOverflowRelatedQuestions.as_view(),
        name="GetStackOverflowRelatedQuestions",
    ),
    path(
        "stack/get/simple_search/<str:page>/<str:pagesize>/<str:fromdate>/<str:todate>/<str:order>/<str:sort>/<str:nottagged>/<str:tagged>/<str:intitle>/<str:token>/",
        views.GetStackOverflowSimpleSearch.as_view(),
        name="GetStackOverflowSimpleSearch",
    ),
    path(
        "stack/get/advanced_search/<str:page>/<str:pagesize>/<str:fromdate>/<str:todate>/<str:order>/<str:sort>/<str:q>/<str:accepted>/<str:answers>/<str:body>/<str:closed>/<str:migrated>/<str:notice>/<str:nottagged>/<str:tagged>/<str:title>/<str:user>/<str:url>/<str:views>/<str:wiki>/<str:token>/",
        views.GetStackOverflowAdvancedSearch.as_view(),
        name="GetStackOverflowAdvancedSearch",
    ),
    path(
        "stack/get/all_tags/",
        views.GetStackOverflowAllTagsInDB.as_view(),
        name="GetStackOverflowAllTagsInDB",
    ),
    path(
        "stack/get/params/all/",
        views.GetAllStackOverflowParams.as_view(),
        name="GetAllStackOverflowParams",
    ),
    path(
        "stack/get/params/<str:route>/",
        views.GetStackOverflowParams.as_view(),
        name="GetStackOverflowParams",
    ),
    path(
        "stack/get/routes/",
        views.GetStackOverflowRoutes.as_view(),
        name="GetStackOverflowRoutes",
    ),
    path(
        "stack/get/filters/all/",
        views.GetAllStackOverflowFilters.as_view(),
        name="GetAllStackOverflowFilters",
    ),
    path(
        "stack/get/filters/<str:route>/",
        views.GetStackOverflowFilters.as_view(),
        name="GetStackOverflowFilters",
    ),
    path(
        "stack/get/sort_methods/",
        views.GetStackOverflowSortMethods.as_view(),
        name="GetStackOverflowSortMethods",
    ),
    path(
        "stack/get/order_methods/",
        views.GetStackOverflowOrderMethods.as_view(),
        name="GetStackOverflowOrderMethods",
    ),
    path(
        "stack/get/question_data_fields/",
        views.GetStackOverflowQuestionDataFields.as_view(),
        name="GetStackOverflowQuestionDataFields",
    ),
    path(
        "stack/get/tags_from_site/<int:pages>/",
        views.GetStackOverflowTagsFromSite.as_view(),
        name="GetStackOverflowTagsFromSite",
    ),
    # Reddit Routes
    # GET data
    # path("reddit/get/sub_reddits/", views.GetSubReddits.as_view()),
    # path("reddit/get/query_types", views.GetRedditQueryTypes.as_view()),
    path(
        "reddit/get/query/<str:search_type>/<str:subred>/<str:q>/<str:limit>/<str:token>/",
        views.GetRedditData.as_view(),
        name="GetRedditData",
    ),
    # Meta Routes
    path(
        "meta/initialisedb/",
        views.InitialiseDatabase.as_view(),
        name="InitialiseDatabase",
    ),
    path(
        "search/stackoverflow/<str:term>/",
        views.StackSearchResponseView.as_view(),
        name="StackOverflowSearch",
    ),
    path(
        "search/reddit/<str:term>/",
        views.RedditSearchResponseView.as_view(),
        name="RedditSearch",
    ),
    path("get-details/", views.UserDetailView.as_view(), name="UserDetail"),
    path("register/", views.RegisterUserView.as_view(), name="RegisterUser"),
    path(
        "searchhistory/<str:token>/",
        views.SearchHistoryView.as_view(),
        name="SearchHistory",
    ),
    path(
        "searchhistory/retrieve-search-results/<str:token>/<str:term>/",
        views.RetrieveSearchResults.as_view(),
        name="RetrieveSearchResults",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
