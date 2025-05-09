from django.views.generic import ListView
from .models import Menu


class MenuListView(ListView):
    model = Menu
    template_name = "menu_app/menu.html"
    context_object_name = "menu_items"

    def get_queryset(self):
        return Menu.objects.all().order_by("categoria")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
