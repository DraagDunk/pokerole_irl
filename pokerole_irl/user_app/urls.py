from django.urls import path, include

from .views import RegisterView, UserProfileView, UserProfileEditView
from worlds_app.views import UserCharacterListView, UserWorldListView
from pokerole_app.views.pokemon_views import UserPokemonListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='user-profile'),
    path('profile/<int:pk>/characters/',
         UserCharacterListView.as_view(), name='user-characters'),
    path('profile/<int:pk>/worlds/',
         UserWorldListView.as_view(), name='user-worlds'),
    path('profile/<int:pk>/pokemon/',
         UserPokemonListView.as_view(), name='user-pokemon'),
    path('profile/<int:pk>/edit/', UserProfileEditView.as_view(),
         name='user-profile-edit'),
    path('profile/', UserProfileView.as_view(), name='user-profile-me'),
    path('', include('django.contrib.auth.urls')),
]
