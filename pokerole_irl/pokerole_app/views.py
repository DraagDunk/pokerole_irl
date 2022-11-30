from django.contrib import messages
from django.contrib.auth import  get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render

from django.views.generic import TemplateView, ListView, CreateView

from .forms import UpdateProfileForm, UpdateUserForm

from .models import PokemonSpecies

# Create your views here.


class MainPageView(TemplateView):
    template_name = "index.html"


class AllSpeciesView(ListView):
    template_name = "allspecies.html"
    model = PokemonSpecies
    context_object_name = "species"

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    success_url = '/'

    model = get_user_model()
    fields = ['username', 'password', 'email']  

class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    
    login_url = '/'
    redirect_field_name = 'suffer'

    def post(self, request):
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)

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


