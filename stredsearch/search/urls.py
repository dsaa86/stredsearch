from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from search import views

urlpatterns = [
    path("add/user/<str:display_name>/<int:user_id>/", views.AddNewUser.as_view()),
    path("get/user/<str:display_name>/", views.GetUserByName.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
