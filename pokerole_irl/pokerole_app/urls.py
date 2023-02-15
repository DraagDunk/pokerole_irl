from django.urls import path

from .views.species_views import SpeciesListView, SpeciesDetailView
from .views.base_views import MainPageView
from .views.pokedex_views import PokedexListView, PokedexEntryListView

urlpatterns = [
    path('', MainPageView.as_view(), name="index"),
    path('species/', SpeciesListView.as_view(), name="all_species"),
    path('species/<int:pk>', SpeciesDetailView.as_view(), name="species"),
    path('pokedexes/', PokedexListView.as_view(), name="pokedex_list"),
    path('pokedexes/<int:pk>', PokedexEntryListView.as_view(), name="pokedex"),
]
