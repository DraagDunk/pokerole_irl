from django.views.generic import ListView

from ..models.pokedex_models import Pokedex, PokedexEntry

class PokedexListView(ListView):
    template_name = "pokedex_list.html"
    model = Pokedex
    context_object_name = "pokedexes"
    paginate_by = 10


class PokedexEntryListView(ListView):
    template_name = "pokedex.html"
    model = PokedexEntry
    context_object_name = "entries"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            pokedex__pk=self.kwargs.get("pk")).order_by("number")
        return queryset.prefetch_related("species")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pokedex"] = Pokedex.objects.get(pk=self.kwargs.get("pk"))
        return context