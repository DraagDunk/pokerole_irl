from django.urls import path, include

from .views import RegisterView, UserProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<str:slug>', UserProfileView.as_view(), name='user-profile'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include('django.contrib.auth.urls')),
]
