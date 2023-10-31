from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from search import views

urlpatterns = [

    # Stack Overflow Routes
    # GET data

    path("stack/get/question_by_tag/<str:page>/<str:pagesize>/<str:fromdate>/<str:todate>/<str:order>/<str:sort>/<str:tags>/", views.GetStackOverflowQuestionsByTag.as_view()),
    path("stack/get/related_questions/<str:page>/<str:pagesize>/<str:fromdate>/<str:todate>/<str:order>/<str:sort>/<str:ids>/", views.GetStackOverflowRelatedQuestions.as_view()),
    path("stack/get/simple_search/<str:page>/<str:pagesize>/<str:fromdate>/<str:todate>/<str:order>/<str:sort>/<str:nottagged>/<str:tagged>/<str:intitle>/", views.GetStackOverflowSimpleSearch.as_view()),
    
    path("stack/get/advanced_search/<str:page>/<str:pagesize>/<str:fromdate>/<str:todate>/<str:order>/<str:sort>/<str:q>/<str:accepted>/<str:answers>/<str:body>/<str:closed>/<str:migrated>/<str:notice>/<str:nottagged>/<str:tagged>/<str:title>/<str:user>/<str:url>/<str:views>/<str:wiki>/", views.GetStackOverflowAdvancedSearch.as_view()),
    
    path("stack/get/all_tags/", views.GetStackOverflowAllTagsInDB.as_view()),
    path("stack/get/params/all/", views.GetAllStackOverflowParams.as_view()),
    path("stack/get/params/<str:route>/", views.GetStackOverflowParams.as_view()),
    path("stack/get/routes/", views.GetStackOverflowRoutes.as_view()),
    path("stack/get/filters/all/", views.GetAllStackOverflowFilters.as_view()),
    path("stack/get/filters/<str:route>/", views.GetStackOverflowFilters.as_view()),
    path("stack/get/sort_methods/", views.GetStackOverflowSortMethods.as_view()),
    path("stack/get/order_methods/", views.GetStackOverflowOrderMethods.as_view()),
    path("stack/get/question_data_fields/", views.GetStackOverflowQuestionDataFields.as_view()),

    # Reddit Routes
    # GET data
    # path("reddit/get/sub_reddits/", views.GetSubReddits.as_view()),
    # path("reddit/get/query_types", views.GetRedditQueryTypes.as_view()),
    # path("reddit/get/query/<str:query_type>/<str:sub_reddit>/<str:query>/<int:limit>/", views.GetRedditQuery.as_view()),

    # Meta Routes
    path("meta/initialisedb/", views.InitialiseDatabase.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
