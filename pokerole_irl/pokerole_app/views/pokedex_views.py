from typing import List
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from ..models.pokedex_models import Pokedex, PokedexEntry
from ..models.species_models import PokemonSpecies, Evolution, MoveSet
from ..models.base_models import Type
from .base_views import NextPageMixin


class PokedexListView(LoginRequiredMixin, NextPageMixin, ListView):
    model = Pokedex
    context_object_name = "pokedexes"
    paginate_by = 10
    template_name = "pokedex_list.html"
    hx_template_name = "partials/pokedex_list_elements.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            pass
        else:
            queryset = queryset.filter(
                Q(owner=self.request.user) | Q(owner__isnull=True)).order_by("name").order_by("owner")
        return queryset


class PokedexCreateView(LoginRequiredMixin, CreateView):
    template_name = "pokedex_add.html"
    model = Pokedex

    fields = ('name', 'owner')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        return super().form_valid(form)


class PokedexUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "pokedex_edit.html"
    model = Pokedex
    context_object_name = "pokedex"

    fields = ('name',)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_superuser or obj.owner == self.request.user:
            return obj
        else:
            raise PermissionDenied("You are not the owner of this pokedex.")


class PokedexDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "confirm_delete_object.html"
    model = Pokedex
    success_url = reverse_lazy('pokedex_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.is_superuser or obj.owner == self.request.user:
            return obj
        else:
            raise PermissionDenied("You are not the owner of this pokedex.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.object.name
        return context


class PokedexEntryListView(LoginRequiredMixin, NextPageMixin, ListView):
    template_name = "pokedex.html"
    hx_template_name = "partials/pokedex_elements.html"
    model = PokedexEntry
    context_object_name = "entries"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            pokedex_id=self.kwargs.get("dex_pk")).order_by("number").prefetch_related("species__primary_type", "species__secondary_type")
        if search := self.request.GET.get("search"):
            queryset = queryset.filter(species__name__icontains=search)
        if type_query := self.request.GET.getlist("types"):
            queryset = queryset.filter(Q(species__primary_type__in=type_query) | Q(
                species__secondary_type__in=type_query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pokedex"] = Pokedex.objects.get(
            pk=self.kwargs.get("dex_pk"))
        context["is_owner"] = self.request.user == context["pokedex"].owner
        context["search_field"] = self.request.GET.get("search", "")
        context["types"] = Type.objects.all()
        return context


class PokedexEntryDetailView(LoginRequiredMixin, DetailView):
    template_name = "species.html"
    model = PokedexEntry
    context_object_name = "entry"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(pokedex_id=self.kwargs.get("dex_pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pokemon"] = self.object.species
        context["evolutions"] = Evolution.objects.filter(
            from_species=context["pokemon"])
        context["preevolution"] = Evolution.objects.filter(
            to_species=context["pokemon"])
        context["moveset"] = MoveSet.objects.filter(
            species=context["pokemon"])
        context["pokedex"] = Pokedex.objects.get(
            pk=self.kwargs.get("dex_pk"))
        context["is_owner"] = self.request.user == context["pokedex"].owner
        return context


class PokedexEntryCreateView(LoginRequiredMixin, CreateView):
    template_name = "pokedex_entry_add.html"
    model = PokedexEntry

    fields = ('species', 'number', 'pokedex', 'rarity', 'description')

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

    def get(self, request, *args, **kwargs):
        self.check_dex(request, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_dex(request, **kwargs)
        return super().post(request, *args, **kwargs)

    def check_dex(self, request, **kwargs):
        self.pokedex = get_object_or_404(
            Pokedex, slug=kwargs.get('dex_slug'))
        if request.user.is_superuser or self.pokedex.owner == request.user:
            return
        else:
            raise PermissionDenied("You are not the owner of this pokedex.")


class PokedexEntryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "pokedex_entry_edit.html"
    model = PokedexEntry

    context_object_name = "entry"

    fields = ("number", "rarity", "description")

    def get_queryset(self):
        qs = super().get_queryset()
        self.pokedex = get_object_or_404(
            Pokedex, slug=self.kwargs.get('dex_slug'))
        if self.request.user.is_superuser or self.pokedex.owner == self.request.user:
            return qs.filter(pokedex=self.pokedex)
        else:
            raise PermissionDenied("You are not the owner of this pokedex.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pokedex"] = self.pokedex
        context["base_species"] = PokemonSpecies.objects.exclude(
            name__contains="(Mega")
        return context


class PokedexEntryDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "confirm_delete_object.html"
    model = PokedexEntry

    def get_queryset(self):
        qs = super().get_queryset()
        self.pokedex = get_object_or_404(
            Pokedex, slug=self.kwargs.get('dex_slug'))
        if self.request.user.is_superuser or self.pokedex.owner == self.request.user:
            return qs.filter(pokedex=self.pokedex)
        else:
            raise PermissionDenied("You are not the owner of this pokedex.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = self.object.species.name
        return context

    def get_success_url(self):
        return reverse("pokedex_entries", kwargs={"dex_slug": self.kwargs.get("dex_slug")})

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        entries = PokedexEntry.objects.filter(
            pokedex__slug=self.kwargs.get("dex_slug"), number__gt=self.object.number)
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
