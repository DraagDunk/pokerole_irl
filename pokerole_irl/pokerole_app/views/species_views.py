from django.views.generic import ListView, DetailView

from ..models.species_models import PokemonSpecies, Evolution, MoveSet

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