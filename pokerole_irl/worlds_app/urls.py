from django.urls import path

from .views import *
from pokerole_app.views.pokemon_views import PokemonCreateView

urlpatterns = [
    path('list/', WorldListView.as_view(), name='world-list'),
    path('add/', WorldCreateView.as_view(), name='world-create'),
    path('<str:slug>/', WorldView.as_view(), name='world'),
    path('<str:world_slug>/character/add/',
         CharacterCreateView.as_view(), name='character-create'),
    path('<str:world_slug>/character/<str:slug>/',
         CharacterView.as_view(), name='character'),
    path('<str:world_slug>/character/<str:char_slug>/pokemon/add/',
         PokemonCreateView.as_view(), name='pokemon_add_for')
]
