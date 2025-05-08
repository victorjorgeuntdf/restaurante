from django.db import models

class Menu(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='menus/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    mesa = models.IntegerField()
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, default="En preparaci\u00f3n")

    def __str__(self):
        return f"Pedido en mesa {self.mesa}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.item.nombre} para pedido {self.pedido.mesa}"
