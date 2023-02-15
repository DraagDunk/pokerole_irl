from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render

from django.views.generic import TemplateView, ListView, CreateView, DetailView
from .forms import UpdateProfileForm, UpdateUserForm, CreateUserForm

from .models import PokemonSpecies, Pokedex, Evolution, MoveSet, PokedexEntry


class MainPageView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('/login')


class SpeciesListView(ListView):
    template_name = "allspecies.html"
    model = PokemonSpecies
    context_object_name = "species"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("dex_id")


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


class RegisterView(CreateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    form_class = CreateUserForm
    template_name = 'registration/register.html'
    success_url = '/login'
    model = get_user_model()


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


class UserProfileView(LoginRequiredMixin, TemplateView):
    # Updates the user profile and info
    template_name = 'users/profile.html'

    login_url = '/'
    redirect_field_name = 'suffer'

    def post(self, request):
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated sucessfully')
            return redirect(to='user-profile')

        return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

    def get(self, request):
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
