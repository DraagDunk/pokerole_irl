from django.urls import path

from .views import RegisterView, UserProfileView, SettingListView, SettingCreateView, SettingView, CharacterView, \
    CharacterCreateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('setting_list/', SettingListView.as_view(), name='setting-list'),
    path('setting_create/', SettingCreateView.as_view(), name='setting-create'),
    path('setting/<int:pk>', SettingView.as_view(), name='setting'),
    path('character_create/', CharacterCreateView.as_view(), name='character-create'),
    path('character/<int:pk>', CharacterView.as_view(), name='character')
]
