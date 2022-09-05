from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from django.views.generic import TemplateView
from django.views import View

# Create your views here.


class MainPageView(TemplateView):
    template_name = "index.html"

class Register(View):
    template_name = 'registration/register.html'

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(MainPageView)

        return render(request, self.template_name, {'form' : form})

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form' : form})