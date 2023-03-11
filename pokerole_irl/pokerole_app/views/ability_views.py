from django.views.generic import ListView, DetailView

from ..models.ability_models import Ability


class AbilityListView(ListView):
    template_name = "ability_list.html"
    model = Ability
    paginate_by = 50

    context_object_name = "abilities"


class AbilityDetailView(DetailView):
    template_name = "ability_detail.html"
    model = Ability

    context_object_name = "ability"
