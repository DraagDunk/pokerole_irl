from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class MainPageView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class NextPageMixin:

    def get_template_names(self):
        self.hx_trigger = self.request.headers.get("Hx-Trigger-Name", None)
        if self.hx_trigger == "load-next-page":
            return self.hx_template_name
        else:
            return self.template_name
