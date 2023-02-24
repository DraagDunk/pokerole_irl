from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from .forms import UpdateProfileForm, UpdateUserForm, CreateUserForm
from .models import Setting, Character

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


class RegisterView(CreateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    form_class = CreateUserForm
    template_name = 'registration/register.html'
    success_url = '/login'
    model = get_user_model()

class SettingListView(LoginRequiredMixin, ListView):
    template_name = "users/setting_list.html"
    model = Setting
    context_object_name = "settings"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(members=self.request.user)

class SettingView(LoginRequiredMixin, DetailView):
    template_name = "users/setting.html"
    model = Setting
    context_object_name = "setting"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SettingView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all charactes in the setting
        context['character_list'] = Character.objects.filter(setting=self.object.id)
        return context



class SettingCreateView(LoginRequiredMixin, CreateView):
    template_name = "users/setting_create.html"
    model = Setting
    fields = ("name", "description", "members")

    def form_valid(self, form):
        prod = form.save(commit=False)
        prod.owner = self.request.user
        prod.save()
        form.save_m2m()
        return redirect("setting", pk=prod.id)

class CharacterView(LoginRequiredMixin, DetailView):
    template_name = "users/character.html"
    model = Character
    context_object_name = "character"

class CharacterCreateView(LoginRequiredMixin, CreateView):
    template_name = "users/character_create.html"
    model = Character
    
    fields = ("name", "description", "setting")
    
    def form_valid(self, form):
        prod = form.save(commit=False)
        prod.owner = self.request.user
        prod.save()
        return redirect("character".format(id=prod.id))
