from django.urls import path

from .views.species_views import SpeciesListView, SpeciesDetailView
from .views.base_views import MainPageView
from .views.pokedex_views import (PokedexListView, PokedexCreateView, PokedexUpdateView, PokedexDeleteView,
                                  PokedexEntryListView, PokedexEntryDetailView, PokedexEntryCreateView, PokedexEntryUpdateView, PokedexEntryDeleteView)
from .views.move_views import MoveListView, MoveDetailView
from .views.ability_views import AbilityListView, AbilityDetailView
from .views.pokemon_views import PokemonDetailView, PokemonCreateView, PokemonUpdateView, PokemonRankUpView

urlpatterns = [
    path('', MainPageView.as_view(), name="index"),
    path('species/', SpeciesListView.as_view(), name="all_species"),
    path('species/<int:pk>/', SpeciesDetailView.as_view(), name="species"),
    path('pokedexes/', PokedexListView.as_view(), name="pokedex_list"),
    path('pokedexes/add/', PokedexCreateView.as_view(), name="pokedex_add"),
    path('pokedexes/<int:pk>/edit/',
         PokedexUpdateView.as_view(), name="pokedex_edit"),
    path('pokedexes/<int:pk>/delete/',
         PokedexDeleteView.as_view(), name="pokedex_delete"),
    path('pokedexes/<int:dex_pk>/entries/',
         PokedexEntryListView.as_view(), name="pokedex_entries"),
    path('pokedexes/<int:dex_pk>/entries/<int:pk>',
         PokedexEntryDetailView.as_view(), name="pokedex_entry"),
    path('pokedexes/<int:dex_pk>/entries/add/',
         PokedexEntryCreateView.as_view(), name="pokedex_entry_add"),
    path('pokedexes/<int:dex_pk>/entries/<int:pk>/edit/',
         PokedexEntryUpdateView.as_view(), name="pokedex_entry_edit"),
    path('pokedexes/<int:dex_pk>/entries/<int:pk>/delete/',
         PokedexEntryDeleteView.as_view(), name="pokedex_entry_delete"),
    path('moves/', MoveListView.as_view(), name="moves"),
    path('moves/<int:pk>/', MoveDetailView.as_view(), name="move"),
    path('abilities/', AbilityListView.as_view(), name="abilities"),
    path('abilities/<int:pk>/', AbilityDetailView.as_view(), name="ability"),
    path('pokemon/add/', PokemonCreateView.as_view(), name="pokemon_add"),
    path('pokemon/<slug:slug>/', PokemonDetailView.as_view(), name="pokemon"),
    path('pokemon/<slug:slug>/rankup',
         PokemonRankUpView.as_view(), name="pokemon_rankup"),
    path('pokemon/<slug:slug>/edit/',
         PokemonUpdateView.as_view(), name="pokemon_edit"),
]
