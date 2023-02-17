from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from ..models.pokedex_models import Pokedex, PokedexEntry
from ..models.species_models import PokemonSpecies


class PokedexListView(ListView):
    template_name = "pokedex_list.html"
    model = Pokedex
    context_object_name = "pokedexes"
    paginate_by = 10


class PokedexCreateView(CreateView):
    template_name = "pokedex_add.html"
    model = Pokedex

    fields = ('name',)


class PokedexUpdateView(UpdateView):
    template_name = "pokedex_edit.html"
    model = Pokedex
    context_object_name = "pokedex"

    fields = ('name',)


class PokedexDeleteView(DeleteView):
    template_name = "confirm_delete_object.html"
    model = Pokedex
    success_url = reverse_lazy('pokedex_list')


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
        context["is_owner"] = self.request.user == context["pokedex"].owner
        return context


class PokedexEntryCreateView(CreateView):
    template_name = "pokedex_entry_add.html"
    model = PokedexEntry

    fields = ('species', 'number', 'pokedex', 'rarity')

    def form_valid(self, form):
        if self.request.POST.get("include_family", "off") == "on":
            add_evolutions(
                form.cleaned_data["species"], form.cleaned_data["number"], form.cleaned_data["pokedex"])
        bump_numbers(form.cleaned_data["number"], form.cleaned_data["pokedex"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pokedex"] = self.pokedex
        context["next_number"] = PokedexEntry.objects.filter(pokedex=self.pokedex).order_by(
            "number").last().number + 1 if self.pokedex.species.exists() else 1
        context["base_species"] = PokemonSpecies.objects.exclude(
            name__contains="(Mega")
        return context

    def dispatch(self, request, *args, **kwargs):
        self.pokedex = Pokedex.objects.get(pk=self.kwargs.get("pk"))
        if request.user.is_superuser or self.pokedex.owner == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("You are not the owner of this pokedex.")


def add_evolutions(species, number, pokedex):
    for i, evolution in enumerate(species.evolutions.all().order_by("number")):
        if evolution.is_mega:
            break
        current_number = number + 1 + i
        evo_entry = PokedexEntry(
            number=number+1+i, species=evolution, pokedex=pokedex)
        bump_numbers(current_number, pokedex)
        evo_entry.save()
        add_evolutions(evolution, current_number, pokedex)


def bump_numbers(number, pokedex):
    entries = PokedexEntry.objects.filter(
        pokedex=pokedex, number__gte=number).iterator()
    for entry in entries:
        curr_number = entry.number
        entry.number = curr_number + 1
        entry.save()
