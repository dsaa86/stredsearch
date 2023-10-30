from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from search import views

urlpatterns = [

    # Stack Overflow Routes
    # GET data
    path("stack/get/question_by_tag/<str:tags>/", views.GetStackOverflowQuestionsByTag.as_view()),
    path("stack/get/related_questions/<str:id>/", views.GetStackOverflowRelatedQuestions.as_view()),
    path("stack/get/simple_search/<str:tags>/<str:exclude_tags>/<str:intitle>/", views.GetStackOverflowSimpleSearch.as_view()),
    path("stack/get/advanced_search/<str:question>/<str:accepted>/<int:answers>/<str:body>/<str:closed>/<str:migrated>/<str:notice>/<str:nottagged>/<str:tagged>/<str:title>/<int:user>/<str:url>/<int:views>/<str:wiki>/", views.GetStackOverflowAdvancedSearch.as_view()),
    path("stack/get/all_tags/", views.GetStackOverflowAllTags.as_view()),
    path("stack/get/params/<str:route>/", views.GetStackOverflowParams.as_view()),
    path("stack/get/routes/", views.GetStackOverflowRoutes.as_view()),
    path("stack/get/filters/<str:route>/", views.GetStackOverflowFilters.as_view()),
    path("stack/get/sort_methods/", views.GetStackOverflowSortMethods.as_view()),
    path("stack/get/order_methods/", views.GetStackOverflowOrderMethods.as_view()),
    path("stack/get/question_data_fields/", views.GetStackOverflowQuestionDataFields.as_view()),

    # Reddit Routes
    # GET data
    path("reddit/get/sub_reddits/", views.GetSubReddits.as_view()),
    path("reddit/get/query_types", views.GetRedditQueryTypes.as_view()),
    path("reddit/get/query/<str:query_type>/<str:sub_reddit>/<str:query>/<int:limit>/", views.GetRedditQuery.as_view()),

    # Meta Routes
]

urlpatterns = format_suffix_patterns(urlpatterns)
