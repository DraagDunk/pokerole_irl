from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied

from ..models.pokedex_models import Pokedex, PokedexEntry
from ..models.species_models import PokemonSpecies, Evolution, MoveSet


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.object.name
        return context


class PokedexEntryListView(ListView):
    template_name = "pokedex.html"
    model = PokedexEntry
    context_object_name = "entries"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            pokedex__pk=self.kwargs.get("dex_pk")).order_by("number")
        return queryset.prefetch_related("species")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pokedex"] = Pokedex.objects.get(pk=self.kwargs.get("dex_pk"))
        context["is_owner"] = self.request.user == context["pokedex"].owner
        return context


class PokedexEntryDetailView(DetailView):
    template_name = "species.html"
    model = PokedexEntry
    context_object_name = "entry"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pokedex__pk=self.kwargs.get("dex_pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pokemon"] = self.object.species
        context["evolutions"] = Evolution.objects.filter(
            from_species=context["pokemon"])
        context["preevolution"] = Evolution.objects.filter(
            to_species=context["pokemon"])
        context["moveset"] = MoveSet.objects.filter(
            species=context["pokemon"])
        context["pokedex"] = Pokedex.objects.get(pk=self.kwargs.get("dex_pk"))
        context["is_owner"] = self.request.user == context["pokedex"].owner
        return context


class PokedexEntryCreateView(CreateView):
    template_name = "pokedex_entry_add.html"
    model = PokedexEntry

    fields = ('species', 'number', 'pokedex', 'rarity')

    def form_valid(self, form):
        bump_count = 1
        queryset = PokedexEntry.objects.all()
        if self.request.POST.get("include_family", "off") == "on":
            evos, _ = add_evolutions(
                form.cleaned_data["species"], form.cleaned_data["number"], form.cleaned_data["pokedex"])
            bump_count = len(evos) + 1
            queryset = queryset.exclude(pk__in=evos)
        bump_numbers(
            form.cleaned_data["number"], form.cleaned_data["pokedex"], queryset, count=bump_count)
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
        self.pokedex = Pokedex.objects.get(pk=self.kwargs.get("dex_pk"))
        if request.user.is_superuser or self.pokedex.owner == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("You are not the owner of this pokedex.")


class PokedexEntryUpdateView(UpdateView):
    template_name = "pokedex_entry_edit.html"
    model = PokedexEntry

    context_object_name = "entry"

    fields = ("number", "rarity")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pokedex"] = Pokedex.objects.get(pk=self.kwargs.get("dex_pk"))
        context["base_species"] = PokemonSpecies.objects.exclude(
            name__contains="(Mega")
        return context


class PokedexEntryDeleteView(DeleteView):
    template_name = "confirm_delete_object.html"
    model = PokedexEntry

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.object.species.name
        return context

    def get_success_url(self):
        return reverse("pokedex_entries", kwargs={"dex_pk": self.kwargs.get("dex_pk")})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        entries = PokedexEntry.objects.filter(
            pokedex__pk=self.kwargs.get("dex_pk"), number__gt=self.object.number)
        for entry in entries.iterator():
            entry.number = entry.number - 1
            entry.save()
        return response


def add_evolutions(species, number, pokedex, i=1):
    evos = []
    for evolution in species.evolutions.all().order_by("number"):
        if evolution.is_mega:
            break
        current_number = number+i
        evo_entry = PokedexEntry(
            number=current_number, species=evolution, pokedex=pokedex)
        evo_entry.save()
        evos.append(evo_entry.pk)
        more_evos, i = add_evolutions(evolution, current_number, pokedex, i)
        evos.extend(more_evos)
        i += 1
    return evos, i


def bump_numbers(number, pokedex, queryset, count=1):
    entries = queryset.filter(
        pokedex=pokedex, number__gte=number).iterator()
    for entry in entries:
        curr_number = entry.number
        entry.number = curr_number + count
        entry.save()
