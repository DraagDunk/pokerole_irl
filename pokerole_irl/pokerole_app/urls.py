from django.urls import path

from .views.species_views import SpeciesListView, SpeciesDetailView
from .views.base_views import MainPageView
from .views.pokedex_views import (PokedexListView, PokedexCreateView, PokedexUpdateView, PokedexDeleteView,
                                  PokedexEntryListView, PokedexEntryDetailView, PokedexEntryCreateView, PokedexEntryUpdateView, PokedexEntryDeleteView)

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
         PokedexEntryDeleteView.as_view(), name="pokedex_entry_delete")
]
