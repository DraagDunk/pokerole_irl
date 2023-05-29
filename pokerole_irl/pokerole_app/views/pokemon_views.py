from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models.pokemon_models import Pokemon


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
