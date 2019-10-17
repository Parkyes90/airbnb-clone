from django.views.generic import ListView

from rooms.models import Room


class HomeView(ListView):
    """
    HomeView Definition
    """

    model = Room
    paginate_by = 10
    ordering = "created"
    paginate_orphans = 5
    context_object_name = "rooms"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
