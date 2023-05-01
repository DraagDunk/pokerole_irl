from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(WorldView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all charactes in the world
        context['character_list'] = Character.objects.filter(world=self.object.id)
        return context


class WorldCreateView(LoginRequiredMixin, CreateView):
    template_name = "world_create.html"
    model = World
    fields = ("__all__")

    def get_success_url(self) -> str:
        return reverse_lazy('world', kwargs={"pk":self.object.pk})

    def form_valid(self, form):
        # set the querying user as the Owner
        response = super().form_valid(form)
        membership, _ = WorldMember.objects.get_or_create(user=self.request.user, world=self.object)
        membership.role = "Owner"
        membership.save()
        return response

class WorldUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "world_update.html"
    model = World
    fields = ("__all__")
    context_object_name = "world"

    def dispatch(self, request, *args, **kwargs):
        self.world = World.objects.get(pk=self.kwargs.get("pk"))
        if request.user.is_superuser or self.world.user == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("You are not the owner of this world.")
    
    def get_success_url(self) -> str:
        return reverse_lazy('world', kwargs={"pk":self.object.pk})
        
class CharacterView(LoginRequiredMixin, DetailView):
    template_name = "character.html"
    model = Character
    context_object_name = "character"

class CharacterCreateView(LoginRequiredMixin, CreateView):
    template_name = "character_create.html"
    model = Character

    fields = ("first_name", "last_name", "description")

    def dispatch(self, request, *args, **kwargs):
        self.world = World.objects.get(pk=self.kwargs.get("world_pk"))

        if request.user.is_superuser or self.request.user in self.world.members.all():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have access to this world")

    def get_success_url(self) -> str:
        return reverse_lazy('character', kwargs={"world_pk":self.object.world.pk, "pk":self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.world = self.world
        return super().form_valid(form)

class CharacterUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "character_update.html"
    model = Character
    fields = ("__all__")
    context_object_name = "character"

    def dispatch(self, request, *args, **kwargs):
        self.world = World.objects.get(pk=self.kwargs.get("world_pk"))
        if request.user.is_superuser or self.owner == request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("You are not the owner of this world.")
        
    def get_success_url(self) -> str:
        return reverse_lazy('character', kwargs={"world_pk":self.object.world.pk, "pk":self.object.pk})