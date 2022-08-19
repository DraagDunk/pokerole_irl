from django.shortcuts import render

from django.views.generic import TemplateView, ListView

from .models import PokemonSpecies

# Create your views here.


class MainPageView(TemplateView):
    template_name = "index.html"


class AllSpeciesView(ListView):
    template_name = "allspecies.html"
    model = PokemonSpecies
    context_object_name = "species"
