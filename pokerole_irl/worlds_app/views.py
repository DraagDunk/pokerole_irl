from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView
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

    def form_valid(self, form):
        # set the querying user as the Owner
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        membership = WorldMember.objects.get(user=self.request.user, world=prod.id)
        membership.role = "Owner"
        membership.save()
        return redirect("world", pk=prod.id)

class CharacterView(LoginRequiredMixin, DetailView):
    template_name = "character.html"
    model = Character
    context_object_name = "character"

class CharacterCreateView(LoginRequiredMixin, CreateView):
    template_name = "character_create.html"
    model = Character
    
    fields = ("first_name", "last_name", "description")
    

    def form_valid(self, form):
        prod = form.save(commit=False)
        prod.owner = self.request.user
        prod.world.id = 1 # HAS TO BE FIXED!!!
        prod.save()
        return redirect("character", pk=prod.id, world_pk=prod.world.id)