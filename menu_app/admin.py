
from django.contrib import admin
from .models import Menu, Pedido, ItemPedido

admin.site.register(Pedido)
admin.site.register(ItemPedido)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'disponible')
    search_fields = ('nombre', 'categoria')
    list_filter = ('categoria', 'disponible')

admin.site.register(Menu, MenuAdmin)

