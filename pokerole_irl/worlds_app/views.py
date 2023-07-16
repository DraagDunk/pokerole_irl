from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.core.exceptions import PermissionDenied
from .models import World, Character, WorldMember



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
    slug_field = 'world_slug'
    slug_url_kwarg = 'world_slug'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(WorldView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all charactes in the world
        context['character_list'] = Character.objects.filter(world=self.object.id)
        return context

    def get_object(self, queryset=None):
        """ Retrieve the object, and check if user is the owner or a superuser """
        obj = super().get_object(queryset)
        if self.request.user not in obj.members.all() and not self.request.user.is_superuser:
            raise PermissionDenied("You are not the owner of this world.")
        return obj


class WorldCreateView(LoginRequiredMixin, CreateView):
    template_name = "world_create.html"
    model = World
    fields = ("name", "members", "description")

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()

    def form_valid(self, form):
        # set the querying user as the Owner
        response = super().form_valid(form)
        membership, _ = WorldMember.objects.get_or_create(
            user=self.request.user, world=self.object)
        membership.role = "Owner"
        membership.save()
        return response


class WorldUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "world_update.html"
    model = World
    fields = ("name", "members", "description")
    context_object_name = "world"
    slug_field = 'world_slug'
    slug_url_kwarg = 'world_slug'

    def dispatch(self, request, *args, **kwargs):
        self.world = World.objects.get(world_slug=self.kwargs.get("world_slug"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return self.object.get_absolute_url()

    def get_object(self, queryset=None):
        """ Retrieve the object, and check if user is the owner or a superuser """
        obj = super().get_object(queryset)
        if self.request.user not in obj.members.all() and not self.request.user.is_superuser:
            raise PermissionDenied("You are not the owner of this world.")
        return obj


class CharacterView(LoginRequiredMixin, DetailView):
    template_name = "character.html"
    model = Character
    context_object_name = "character"
    slug_field = 'character_slug'
    slug_url_kwarg = 'character_slug'

    def get_object(self, queryset=None):
        """ Retrieve the object, and check if user is the owner or a superuser """
        obj = super().get_object(queryset)
        if not obj.owner == self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("You are not the owner of this character")
        return obj


class CharacterCreateView(LoginRequiredMixin, CreateView):
    template_name = "character_create.html"
    model = Character

    fields = ("first_name", "last_name", "description")

    def dispatch(self, request, *args, **kwargs):
        self.world = World.objects.get(world_slug=self.kwargs.get(
            "world_slug"))

        if request.user.is_superuser or self.request.user in self.world.members.all():
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have access to this world")

    def get_success_url(self) -> str:
        return reverse_lazy('character', kwargs={
            "world_slug": self.object.world.world_slug,
            "character_slug": self.object.character_slug})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.world = self.world
        return super().form_valid(form)


class CharacterUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "character_update.html"
    model = Character
    fields = ("owner", "world", "first_name", "last_name", "description")
    context_object_name = "character"
    slug_field = 'character_slug'
    slug_url_kwarg = 'character_slug'
    def dispatch(self, request, *args, **kwargs):
        self.world = World.objects.get(world_slug=self.kwargs.get(
            "world_slug"))
        return super().dispatch(request, *args, **kwargs)


    def get_success_url(self) -> str:
        return reverse_lazy('character', kwargs={
            "world_slug": self.object.world.world_slug,
            "character_slug": self.object.character_slug})

    def get_object(self, queryset=None):
        """ Retrieve the object, and check if user is the owner or a superuser """
        obj = super().get_object(queryset)
        if not obj.owner == self.request.user and not self.request.user.is_superuser:
            raise PermissionDenied("You are not the owner of this character")
        return obj
