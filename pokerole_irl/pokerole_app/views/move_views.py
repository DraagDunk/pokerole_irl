from django.views.generic import ListView, DetailView

from ..models.move_models import Move

class MoveListView(ListView):
    template_name = "move_list.html"
    model = Move
    paginate_by = 50

    context_object_name = "moves"

class MoveDetailView(DetailView):
    template_name = "move_detail.html"
    model = Move

    context_object_name = "move"