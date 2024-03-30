
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from ..forms import PokemonCreateForm, PokemonEditForm
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


class PokemonCreateView(LoginRequiredMixin, CreateView):
    model = Pokemon
    template_name = "pokemon_add.html"
    form_class = PokemonCreateForm

    def get_success_url(self):
        return reverse_lazy('pokemon_edit', args=(self.object.slug,))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class PokemonUpdateView(LoginRequiredMixin, UpdateView):
    model = Pokemon
    template_name = "pokemon_edit.html"
    form_class = PokemonEditForm
    context_object_name = "pokemon"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["species"] = self.object.species
        context["max_skill"] = min(self.object.rank+1, 5)
        return context


class PokemonRankUpView(LoginRequiredMixin, UpdateView):
    model = Pokemon
    fields = ()

    def post(self, request, *args, **kwargs):
        _ = super().post(request, *args, **kwargs)
        # Cannot rank further than the highest rank.
        if self.object.rank < 6:
            self.object.rank += 1
            self.object.save()
        redirect_url = reverse_lazy(
            'pokemon', kwargs={"slug": self.object.slug})
        return HttpResponseRedirect(redirect_url)
