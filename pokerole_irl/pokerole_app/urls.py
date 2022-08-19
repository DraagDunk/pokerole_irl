from django.urls import path

from .views import AllSpeciesView, MainPageView

urlpatterns = [
    path('', MainPageView.as_view(), name="index"),
    path('all_species/', AllSpeciesView.as_view(), name="all_species"),
]
