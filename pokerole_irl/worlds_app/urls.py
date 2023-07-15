from django.urls import path

from .views import *

urlpatterns = [
    path('list/', WorldListView.as_view(), name='world-list'),
    path('add/', WorldCreateView.as_view(), name='world-create'),
    path('<slug:world_slug>/', WorldView.as_view(), name='world'),
    path('<slug:world_slug>/update', WorldUpdateView.as_view(),
         name='world-update'),
    path('<slug:world_slug>/character/add/', CharacterCreateView.as_view(),
         name='character-create'),
    path('<slug:world_slug>/character/<slug:character_slug>/',
         CharacterView.as_view(), name='character'),
    path('<slug:world_slug>/character/<slug:character_slug>/update',
         CharacterUpdateView.as_view(), name='character-update')
]