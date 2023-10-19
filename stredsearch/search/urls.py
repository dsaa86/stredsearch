from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from search import views

urlpatterns = [
    path('search/', views.QuestionList.as_view()),
    path('reddit/<str:subred>/<str:q>/<str:type>/<str:limit>/', views.GetRedditData.as_view()),
    path('stackoverflow/<str:route>/<str:page>/<str:pagesize>/<str:fromdate>/<str:todate>/<str:order>/<str:min>/<str:max>/<str:sort>/<str:tagged>/', views.GetStackoverflowData.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)