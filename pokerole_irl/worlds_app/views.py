from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, DetailView
from .models import Setting, Character, WorldMember

# Create your views here.

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
    fields = ("__all__")

    def form_valid(self, form):
        prod = form.save(commit=False)
        prod.save()
        form.save_m2m()
        membership = WorldMember.objects.get(user=self.request.user, setting=prod.id)
        membership.role = "Owner"
        membership.save()
        return redirect("setting", pk=prod.id)

class CharacterView(LoginRequiredMixin, DetailView):
    template_name = "users/character.html"
    model = Character
    context_object_name = "character"

class CharacterCreateView(LoginRequiredMixin, CreateView):
    template_name = "users/character_create.html"
    model = Character
    
    fields = ("first_name", "last_name", "description", "setting")
    
    def form_valid(self, form):
        prod = form.save(commit=False)
        prod.owner = self.request.user
        prod.save()
        return redirect("character", pk=prod.id)