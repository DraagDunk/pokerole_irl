from django.urls import path

from .views import MainPageView

urlpatterns = [
    path('', MainPageView.as_view(), name="index")
]
