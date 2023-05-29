from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class MainPageView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
