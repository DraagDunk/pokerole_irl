from django.urls import path, include

from .views import RegisterView, UserProfileView, UserProfileEditView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='user-profile'),
    path('profile/<int:pk>/edit/', UserProfileEditView.as_view(),
         name='user-profile-edit'),
    path('profile/', UserProfileView.as_view(), name='user-profile-me'),
    path('', include('django.contrib.auth.urls')),
]
