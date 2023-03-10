from django.urls import path

from .views import *

urlpatterns = [
    path('list/', WorldListView.as_view(), name='world-list'),
    path('add/', WorldCreateView.as_view(), name='world-create'),
    path('<int:pk>/', WorldView.as_view(), name='world'),
    path('<int:world_pk>/character/add/', CharacterCreateView.as_view(), name='character-create'),
    path('<int:world_pk>/character/<int:pk>/', CharacterView.as_view(), name='character')
]