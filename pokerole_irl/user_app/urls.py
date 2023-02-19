from django.urls import path

from .views import RegisterView, UserProfileView, SettingListView, SettingCreateView, SettingView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('setting_list/', SettingListView.as_view(), name='setting-list'),
    path('setting_create/', SettingCreateView.as_view(), name='setting-create'),
    path('setting_<pk>/', SettingView.as_view(), name='setting')
]
