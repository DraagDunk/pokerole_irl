from django.urls import path

from .views import SpeciesListView, SpeciesDetailView, MainPageView, RegisterView, PokedexListView, PokedexDetailView, UserProfileView

urlpatterns = [
    path('', MainPageView.as_view(), name="index"),
    path('species/', SpeciesListView.as_view(), name="all_species"),
    path('species/<int:pk>', SpeciesDetailView.as_view(), name="species"),
    path('pokedexes/', PokedexListView.as_view(), name="pokedex_list"),
    path('pokedexes/<int:pk>', PokedexDetailView.as_view(), name="pokedex"),
    path('register', RegisterView.as_view(), name='register'),
    path('accounts/profile/', UserProfileView.as_view(), name='user-profile')
]
