from django.views.generic import ListView, DetailView

from ..models.species_models import PokemonSpecies, Evolution, MoveSet


class SpeciesListView(ListView):
    model = PokemonSpecies
    context_object_name = "species"
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        self.hx_trigger = request.headers.get("Hx-Trigger-Name", None)
        response = super().get(request, *args, **kwargs)

        return response

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("dex_id")

    def get_template_names(self):
        if self.hx_trigger == "load-next-page":
            return "partials/allspecies_elements.html"
        else:
            return "allspecies.html"


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
