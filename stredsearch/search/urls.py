from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from search import views

urlpatterns = [
    path("user/<str:name>/", views.AddNewUser),
]

urlpatterns = format_suffix_patterns(urlpatterns)
