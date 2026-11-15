from django.urls import path

from . import views

app_name = "team"

urlpatterns = [
    path("", views.team_list, name="list"),
    path("add/", views.add_pokemon, name="add"),
    path("pokemon/<int:pk>/", views.pokemon_detail, name="detail"),
    path("pokemon/<int:pk>/remove/", views.remove_pokemon, name="remove"),
    path("search/", views.search, name="search"),
    path("battle/", views.battle, name="battle"),
]
