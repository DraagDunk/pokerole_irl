from urllib import request
from django.shortcuts import render

from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import TemplateView, ListView, CreateView, View

from .models import PokemonSpecies

# Create your views here.


class MainPageView(TemplateView):
    template_name = "index.html"


class AllSpeciesView(ListView):
    template_name = "allspecies.html"
    model = PokemonSpecies
    context_object_name = "species"

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    success_url = '/'

    model = get_user_model()
    fields = ['username', 'password']  

class UserProfileView(LoginRequiredMixin, TemplateView):
    login_url = '/'
    redirect_field_name = 'suffer'

    template_name = 'users/profile.html'