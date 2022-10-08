from django.urls import path

from .views import AllSpeciesView, MainPageView, RegisterView, UserProfileView

urlpatterns = [
    path('', MainPageView.as_view(), name="index"),
    path('all_species/', AllSpeciesView.as_view(), name="all_species"),
    path('register', RegisterView.as_view(), name='register'),
    path('accounts/profile/', UserProfileView.as_view(), name='user-profile')
]
