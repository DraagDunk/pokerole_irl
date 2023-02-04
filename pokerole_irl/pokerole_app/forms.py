from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from .models import Profile

# Form that creates a user


class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {"username": UsernameField,
                         "email": forms.EmailField}

# Form that updates user information


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']

# Form that updates user profile


class UpdateProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['bio']
