from django.shortcuts import render
from .models import Menu

def menu_view(request):
    # Obtener todos los ítems del menú
    menu_items = Menu.objects.all()
    return render(request, 'menu_app/menu.html', {'menu_items': menu_items})
