from django.urls import path

from .views import AllSpeciesView, MainPageView, RegisterView, profile, TestView

urlpatterns = [
    path('', MainPageView.as_view(), name="index"),
    path('all_species/', AllSpeciesView.as_view(), name="all_species"),
    path('register', RegisterView.as_view(), name='register'),
    path('accounts/profile/', TestView.as_view(), name='user-profile')
]
