from typing import Any
from django import http
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView, ListView
from friendship.models import Friend, Follow, Block

from .forms import UpdateProfileForm, UpdateUserForm, CreateUserForm


def get_friendship_context_object_name():
    return getattr(settings, "FRIENDSHIP_CONTEXT_OBJECT_NAME", "user")


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

        return render(request, 'users/profile.html', 
                      {'user_form': user_form, 'profile_form': profile_form})

    def get(self, request):
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

        return render(request, 'users/profile.html',
                      {'user_form': user_form, 'profile_form': profile_form})


class RegisterView(CreateView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

    form_class = CreateUserForm
    template_name = 'registration/register.html'
    success_url = '/login'
    model = get_user_model()


class FriendListView(LoginRequiredMixin, TemplateView):
    template_name = 'friend_list.html'

    def get(self, request):
        friends = Friend.objects.friends(request.user)
        return render(request, self.template_name, {
            get_friendship_context_object_name(): request.user,
            "friendship_context_object_name": get_friendship_context_object_name(),
            "friends": friends,
        })
