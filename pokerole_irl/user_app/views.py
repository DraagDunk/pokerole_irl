from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import UpdateProfileForm, UpdateUserForm, CreateUserForm
from .models import Profile


class UserProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user
        context['owned'] = context['user'] == self.request.user
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs.get('pk') is None:
            self.kwargs['pk'] = request.user.profile.pk
        return super().dispatch(request, *args, **kwargs)


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    context_object_name = "profile"
    template_name = "profile_edit.html"
    fields = ('bio',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user
        context["user_form"] = UpdateUserForm(instance=self.object.user)
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or self.kwargs.get('pk') == request.user.profile.pk:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied(
                "You are not the owner of this profile!")

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        post_vals = {key: val for key, val in request.POST.items()}
        post_vals['username'] = self.object.user.username
        user_form = UpdateUserForm(post_vals, instance=self.object.user)

        if user_form.is_valid():
            user_form.save()

        return response


class RegisterView(CreateView):
    form_class = CreateUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    model = get_user_model()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
