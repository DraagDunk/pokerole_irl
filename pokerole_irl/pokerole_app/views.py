from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, get_user_model

from django.views.generic import TemplateView, ListView, CreateView, DetailView

from .models import PokemonSpecies, Pokedex, Evolution, MoveSet


class MainPageView(TemplateView):
    template_name = "index.html"


class SpeciesListView(ListView):
    template_name = "allspecies.html"
    model = PokemonSpecies
    context_object_name = "species"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("dex_id")


class SpeciesDetailView(DetailView):
    template_name = "species.html"
    model = PokemonSpecies
    context_object_name = "pokemon"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["evolutions"] = Evolution.objects.filter(
            from_species=context["pokemon"])
        context["preevolution"] = Evolution.objects.filter(
            to_species=context["pokemon"])
        context["moveset"] = MoveSet.objects.filter(
            species=context["pokemon"])
        return context


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    success_url = '/'

    model = get_user_model()
    fields = ['username', 'password']


class PokedexListView(ListView):
    template_name = "pokedex_list.html"
    model = Pokedex
    context_object_name = "pokedexes"
    paginate_by = 10


class PokedexDetailView(DetailView):
    template_name = "pokedex.html"
    model = Pokedex
    context_object_name = "pokedex"

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset)
        return queryset.prefetch_related("pokedexentry_set")
