from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, get_user_model

from django.views.generic import TemplateView, ListView, CreateView

from .models import PokemonSpecies

# Create your views here.


class MainPageView(TemplateView):
    template_name = "index.html"


class AllSpeciesView(ListView):
    template_name = "allspecies.html"
    model = PokemonSpecies
    context_object_name = "species"
    paginate_by = 20


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    success_url = '/'

    model = get_user_model()
    fields = ['username', 'password']
