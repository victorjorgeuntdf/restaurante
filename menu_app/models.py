from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# -------------------------------------------------------
# models.py
# Definición de modelos para User, Notification, Booking, Category, Product, Table, Rating, Order y TimeSlot.
# Custom User model
# Extendiendo AbstractUser para añadir campos adicionales
# relación many-to-many con Notification.
# relaciones one-to-many con Booking, Order y Rating.
# realciones de one-to-many entre Booking y Table.
# relación one-to-many entre Product y Rating.
# realción one-to-many entre Category y Product.
# realción many-to-many entre Table y TimeSlot a través de TableTimeSlot.
# relación many-to-many entre Order y Product a través de OrderProduct.
# PRODUCT MODEL FUSIONADO con ejemplo de validaciones,
# creación y actualización.
# Recuerda en settings.py definir:
# AUTH_USER_MODEL = 'yourapp.User'
# -------------------------------------------------------

class User(AbstractUser):
    """
    Modelo de usuario personalizado.

    Atributos heredados de AbstractUser:
      - username
      - email
      - first_name
      - last_name
      - password
      - ...

    Atributos adicionales:
      - phone: teléfono de contacto opcional
    """
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Número de teléfono del usuario (opcional)."
    )

    # Relación many-to-many con Notification a través de UserNotification
    notifications = models.ManyToManyField(
        'Notification',                      # Modelo relacionado
        through='UserNotification',           # Modelo intermedio
        related_name='users',                 # Nombre inverso para consultas
        blank=True,
        help_text="Notificaciones asociadas al usuario."
    )

    # Relación one-to-many: un usuario puede tener múltiples reservas (Booking)
    # A través de ForeignKey definida en Booking (related_name='bookings')

    def __str__(self):
        return self.username


# -------------------------------------------------------
# Notification model
# Representa una notificación que puede enviarse a varios usuarios
# -------------------------------------------------------
class Notification(models.Model):
    """
    Modelo de notificación.

    Atributos:
      - title: título breve de la notificación
      - message: contenido detallado
      - created_at: fecha de creación (auto)
      - is_read: indicador de lectura
    """
    title = models.CharField(
        max_length=255,
        help_text="Título de la notificación."
    )
    message = models.TextField(
        help_text="Mensaje o contenido de la notificación."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora en que se creó la notificación."
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Indica si la notificación ha sido marcada como leída."
    )

    def __str__(self):
        estado = 'Leída' if self.is_read else 'No leída'
        return f"{self.title} ({estado})"


# -------------------------------------------------------
# Intermediate model: UserNotification
# Tabla intermedia para la relación many-to-many.
# -------------------------------------------------------
class UserNotification(models.Model):
    """
    Modelo intermedio que vincula User y Notification.

    Atributos:
      - user: referencia al modelo User
      - notification: referencia al modelo Notification

    Permite añadir campos adicionales en la relación,
    como timestamps específicos por usuario-notificación.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text="Usuario que recibe la notificación."
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        help_text="Notificación asociada al usuario."
    )
    # Ejemplo de campo adicional en la tabla intermedia:
    # received_at = models.DateTimeField(auto_now_add=True,
    #     help_text="Fecha en que el usuario recibió la notificación.")

    class Meta:
        # Evitar duplicados de la misma notificación para un usuario
        unique_together = ('user', 'notification')
        verbose_name = 'User Notification'
        verbose_name_plural = 'User Notifications'

    def __str__(self):
        return f"Notificación '{self.notification.title}' para {self.user.username}"


# -------------------------------------------------------
# Booking model
# Representa una reserva asociada a un usuario.
# -------------------------------------------------------
class Booking(models.Model):
    """
    Modelo que representa una reserva (booking).

    Atributos:
      - user: usuario que realiza la reserva (ForeignKey)
      - approved: indica si la reserva fue aprobada
      - approval_date: fecha de aprobación (puede ser nula)
      - code: código único de la reserva
      - observations: comentarios u observaciones
      - date: fecha de la reserva
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  #Esta es una entidad débil
        related_name='bookings',
        help_text="Usuario que realizó la reserva."
    )
    approved = models.BooleanField(
        default=False,
        help_text="Marca si la reserva fue aprobada."
    )
    approval_date = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha en que se aprobó la reserva."
    )
    code = models.CharField(
        max_length=100,
        unique=True,
        help_text="Código único de la reserva."
    )
    observations = models.TextField(
        blank=True,
        help_text="Comentarios u observaciones sobre la reserva."
    )
    date = models.DateField(
        help_text="Fecha programada de la reserva."
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"Booking {self.code} - {self.user.username}"


# -------------------------------------------------------
# Order model
# Representa un pedido realizado por un usuario.
# Pedido que puede incluir múltiples productos.
# -------------------------------------------------------
class Order(models.Model):
    """
    Modelo que representa un pedido (Order).

    Atributos:
      - user: usuario que realizó el pedido (ForeignKey)
      - buy_date: fecha de compra
      - code: código único del pedido
      - amount: monto total del pedido
      - state: estado del pedido
      - products: productos incluidos en el pedido (ManyToMany)
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, #Esta es una entidad débil
        related_name='orders',
        help_text="Usuario que generó el pedido."
    )
    buy_date = models.DateField(
        help_text="Fecha en que se realizó la compra."
    )
    code = models.CharField(
        max_length=100,
        unique=True,
        help_text="Código único identificador del pedido."
    )
    amount = models.FloatField(
        help_text="Importe total del pedido."
    )
    STATE_CHOICES = [
        ('PREPARACION', 'Preparación'),
        ('ENVIADO', 'Enviado'),
        ('RECIBIDO', 'Recibido'),
        ('CANCELADO', 'Cancelado'),
    ]
    state = models.CharField(
        max_length=12,
        choices=STATE_CHOICES,
        default='PREPARACION',
        help_text="Estado actual del pedido."
    )
    
    # Many-to-Many con Product
    products = models.ManyToManyField(
        'Product',
        through='OrderProduct',
        related_name='orders',
        help_text="Productos incluidos en el pedido."
    )
    class Meta:
        ordering = ['-buy_date']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order {self.code} - {self.user.username}"


# -------------------------------------------------------
# Category model
# Representa una categoría de productos.
# -------------------------------------------------------
class Category(models.Model):
    """
    Modelo que representa una categoría de productos.

    Atributos:
      - name: nombre de la categoría
      - description: descripción de la categoría
      - is_active: si la categoría está activa
    """
    name = models.CharField(
        max_length=255,
        help_text="Nombre de la categoría."
    )
    description = models.TextField(
        blank=True,
        help_text="Descripción de la categoría."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indica si la categoría está activa."
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# -------------------------------------------------------
# Product model
# Representa un producto que puede recibir valoraciones.
# Representa un producto que pertenece a una categoría.
# -------------------------------------------------------
class Product(models.Model):
    """
    Producto del catálogo, con validaciones y métodos auxiliares.

    Atributos:
      - category: categoría (ForeignKey)
      - name: nombre
      - description: descripción
      - price: precio (DecimalField)
      - quantity: stock
      - image: imagen opcional
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        null=True,          # <–– permite valores NULL en la BD
        blank=True,         # <–– permite dejarlos vacíos en formularios/admin
        help_text="Categoría a la que pertenece el producto."
    )

    name = models.CharField(
        max_length=255,
        help_text="Nombre del producto."
    )
    description = models.TextField(
        help_text="Descripción detallada del producto."
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Precio del producto."
    )
    quantity = models.IntegerField(
        help_text="Cantidad disponible en stock."
    )

    image = models.ImageField(
        upload_to='products/', 
        null=True, 
        blank=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    @classmethod
    def validate(cls, name, description, price):
        errors = {}
        if not name:
            errors['name'] = 'Por favor ingrese un nombre'
        if not description:
            errors['description'] = 'Por favor ingrese una descripción'
        if price is None or price <= 0:
            errors['price'] = 'Por favor ingrese un precio mayor a 0'
        return errors

    @classmethod
    def new(cls, category, name, description, price, quantity, image=None):
        errors = cls.validate(name, description, price)
        if errors:
            return False, errors
        cls.objects.create(
            category=category,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            image=image
        )
        return True, None

    def update(self, category=None, name=None, description=None, price=None, quantity=None, image=None):
        self.category = category or self.category
        self.name = name or self.name
        self.description = description or self.description
        self.price = price or self.price
        self.quantity = quantity or self.quantity
        if image is not None:
            self.image = image
        self.save()

# -------------------------------------------------------
# Rating model
# Representa una calificación realizada por un usuario.
# Representa una valoración de usuario para un producto.
# -------------------------------------------------------
class Rating(models.Model):
    """
    Modelo que representa una valoración o reseña.
    Valoración o reseña asociada a un producto y usuario.

    Atributos:
      - user: usuario que realizó la calificación (ForeignKey)
      - product: producto valorado (ForeignKey)
      - title: título de la calificación
      - text: texto o comentarios de la calificación
      - rating: valor numérico de la calificación
      - created_at: fecha y hora de creación
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, #Esta es una entidad débil
        related_name='ratings',
        help_text="Usuario que realizó la calificación."
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='ratings',
        help_text="Producto al que pertenece la calificación."
    )
    title = models.CharField(
        max_length=255,
        help_text="Título de la calificación."
    )
    text = models.TextField(
        help_text="Texto o comentarios de la calificación."
    )
    rating = models.PositiveIntegerField(
        help_text="Valor de la calificación (por ejemplo, de 1 a 5)."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación de la calificación."
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    def __str__(self):
        return f"Rating {self.rating} - {self.user.username} on {self.product.title}: {self.title}"
    

# -------------------------------------------------------
# Table model
# Representa una mesa asignada a una reserva (Booking)
# y asociada a múltiples intervalos de tiempo (TimeSlot).
# -------------------------------------------------------
class Table(models.Model):
    """
    Modelo que representa una mesa.
    Mesa que puede asignarse a múltiples intervalos de tiempo (TimeSlot).

    Atributos:
      - booking: reserva asociada (ForeignKey)
      - capacity: número de comensales que admite
      - description: descripción de la mesa
      - is_reserved: si está reservada actualmente
      - timeslots: intervalos de tiempo disponibles (ManyToMany)
    """
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE, # Esta es una entidad débil
        related_name='tables',
        help_text="Reserva a la que pertenece la mesa."
    )
    capacity = models.IntegerField(
        help_text="Capacidad de la mesa (número de personas)."
    )
    description = models.CharField(
        max_length=255,
        help_text="Descripción o ubicación de la mesa."
    )
    is_reserved = models.BooleanField(
        default=True,
        help_text="Indica si la mesa está reservada."
    )

    # Relación many-to-many con TimeSlot a través de TableTimeSlot
    timeslots = models.ManyToManyField(
        'TimeSlot',
        through='TableTimeSlot',
        related_name='tables',
        help_text="Intervalos de tiempo asociados a la mesa."
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'

    def __str__(self):
        return f"Table {self.id} ({self.capacity} pax)"


# -------------------------------------------------------
# TimeSlot model
# Representa intervalos de tiempo disponibles para mesas.
# -------------------------------------------------------
class TimeSlot(models.Model):
    """
    Intervalo de tiempo para reservas de mesas.

    Atributos:
      - start: inicio del intervalo
      - end: fin del intervalo
      - is_full: si el intervalo está completo
    """
    start = models.DateTimeField(
        help_text="Fecha y hora de inicio del intervalo."
    )
    end = models.DateTimeField(
        help_text="Fecha y hora de fin del intervalo."
    )
    is_full = models.BooleanField(
        default=False,
        help_text="Indica si el intervalo de tiempo está completo."
    )

    class Meta:
        ordering = ['start']
        verbose_name = 'TimeSlot'
        verbose_name_plural = 'TimeSlots'

    def __str__(self):
        return f"{self.start} - {self.end}"


# -------------------------------------------------------
# TableTimeSlot model
# Tabla intermedia para la relación Many-to-Many
# entre Table y TimeSlot.
# -------------------------------------------------------
class TableTimeSlot(models.Model):
    """
    Modelo intermedio que relaciona mesas con slots de tiempo.

    Atributos:
      - table: referencia a Table
      - timeslot: referencia a TimeSlot
    """
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        help_text="Mesa asociada al intervalo de tiempo."
    )
    timeslot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        help_text="Intervalo de tiempo asociado a la mesa."
    )

    class Meta:
        unique_together = ('table', 'timeslot')
        verbose_name = 'Table TimeSlot'
        verbose_name_plural = 'Table TimeSlots'

    def __str__(self):
        return f"Table {self.table.id} @ {self.timeslot.start}"


# -------------------------------------------------------
# Tabla intermedia OrderProduct
# Relaciona Order y Product (Many-to-Many).
# -------------------------------------------------------
class OrderProduct(models.Model):
    """
    Tabla intermedia para Order <-> Product.

    Atributos:
      - order: referencia a Order
      - product: referencia a Product
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        help_text="Pedido asociado."
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        help_text="Producto asociado."
    )

    class Meta:
        unique_together = ('order', 'product')
        verbose_name = 'Order Product'
        verbose_name_plural = 'Order Products'

    def __str__(self):
        return f"Order {self.order.code} - Product {self.product.title}"

# -------------------------------------------------------

