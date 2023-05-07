from django.urls import path

from .views import RegisterView, UserProfileView, FriendListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('friends/list', FriendListView.as_view(), name='friend-list')
]
