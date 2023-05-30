from typing import Any, Dict
from django.views.generic import DetailView, CreateView
from django.forms import ModelForm
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models.pokemon_models import Pokemon
from worlds_app.models import Character


class PokemonDetailView(LoginRequiredMixin, DetailView):
    model = Pokemon
    template_name = "pokemon.html"
    context_object_name = "pokemon"

    def get_queryset(self):
        return super().get_queryset().select_related('species')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["owner"] = self.object.owner
        context["trainer"] = self.object.trainer
        context["nature"] = self.object.pokemon_nature
        context["moves"] = self.object.moves.all(
        ).select_related('move_type')
        return context


class PokemonCreateForm(ModelForm):
    class Meta:
        model = Pokemon
        fields = ("nickname", "species", "pokemon_nature", "rank", "trainer")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['trainer'].queryset = Character.objects.filter(owner=user)


class PokemonCreateView(LoginRequiredMixin, CreateView):
    model = Pokemon
    template_name = "pokemon_add.html"
    form_class = PokemonCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
