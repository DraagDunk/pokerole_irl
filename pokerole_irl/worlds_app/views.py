from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.core.exceptions import PermissionDenied
from .models import World, Character, WorldMember

# Create your views here.


class WorldListView(LoginRequiredMixin, ListView):
    template_name = "world_list.html"
    model = World
    context_object_name = "worlds"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(members=self.request.user)


class WorldView(LoginRequiredMixin, DetailView):
    template_name = "world.html"
    model = World
    context_object_name = "world"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(members=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(WorldView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all charactes in the world
        context['character_list'] = Character.objects.filter(
            world=self.object)
        return context


class WorldCreateView(LoginRequiredMixin, CreateView):
    template_name = "world_create.html"
    model = World
    fields = ("__all__")

    def get_success_url(self) -> str:
        return reverse_lazy('world', kwargs={"slug": self.object.slug})

    def form_valid(self, form):
        # set the querying user as the Owner
        response = super().form_valid(form)
        membership, _ = WorldMember.objects.get_or_create(
            user=self.request.user, world=self.object)
        membership.role = "Owner"
        membership.save()
        return response


class CharacterView(LoginRequiredMixin, DetailView):
    template_name = "character.html"
    model = Character
    context_object_name = "character"

    def get_queryset(self):
        allowed_worlds = World.objects.filter(members=self.request.user)
        self.world = get_object_or_404(
            allowed_worlds, slug=self.kwargs.get('world_slug'))
        qs = super().get_queryset()
        return qs.filter(world=self.world)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['world'] = self.world
        return context


class CharacterCreateView(LoginRequiredMixin, CreateView):
    template_name = "character_create.html"
    model = Character

    fields = ("first_name", "last_name", "description")

    def get(self, request, *args, **kwargs):
        self.check_world(request, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.check_world(request, **kwargs)
        return super().post(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy('character', kwargs={"world_slug": self.object.world.slug, "slug": self.object.slug})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.world = self.world
        return super().form_valid(form)

    def check_world(self, request, **kwargs):
        allowed_worlds = World.objects.filter(members=request.user)
        self.world = get_object_or_404(
            allowed_worlds, slug=kwargs.get("world_slug"))
