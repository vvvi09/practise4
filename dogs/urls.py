from django.urls import path

from . import views


urlpatterns = [
    path("", views.breed_list, name="breed_list"),
]