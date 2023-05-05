from django.urls import path

from .views import *

urlpatterns = [
    path('list/', WorldListView.as_view(), name='world-list'),
    path('add/', WorldCreateView.as_view(), name='world-create'),
    path('<str:slug>/', WorldView.as_view(), name='world'),
    path('<str:world_slug>/character/add/', CharacterCreateView.as_view(), name='character-create'),
    path('<str:world_slug>/character/<str:slug>/', CharacterView.as_view(), name='character')
]