from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

class MainPageView(TemplateView):
    template_name = "index.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('login'))
        
