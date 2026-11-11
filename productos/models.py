from decimal import Decimal

from django.db import models
from django.urls import reverse


class ProductoQuerySet(models.QuerySet):
    """Consultas reutilizables del catalogo.

    La logica de negocio vive aqui (capa Model) y no en las vistas.
    Todos los metodos devuelven QuerySets, por lo que son *lazy*:
    no se ejecuta SQL hasta que se itera, se usa len(), list(), etc.
    """

    def disponibles(self):
        return self.filter(disponible=True, stock__gt=0)

    def por_categoria(self, categoria):
        if categoria:
            return self.filter(categoria=categoria)
        return self

    def stock_bajo(self, limite=10):
        return self.filter(stock__lte=limite)

    def buscar(self, texto):
        if texto:
            return self.filter(nombre__icontains=texto)
        return self


class Producto(models.Model):
    class Categoria(models.TextChoices):
        ABARROTES = 'ABA', 'Abarrotes'
        BEBIDAS = 'BEB', 'Bebidas'
        LACTEOS = 'LAC', 'Lácteos'
        LIMPIEZA = 'LIM', 'Limpieza'
        SNACKS = 'SNA', 'Snacks y golosinas'

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(
        max_length=3, choices=Categoria.choices, default=Categoria.ABARROTES
    )
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    objects = ProductoQuerySet.as_manager()

    class Meta:
        ordering = ['categoria', 'nombre']
        verbose_name = 'producto'
        verbose_name_plural = 'productos'

    def __str__(self):
        return f'{self.nombre} (S/ {self.precio})'

    def get_absolute_url(self):
        return reverse('productos:detalle', kwargs={'pk': self.pk})

    @property
    def stock_bajo(self):
        return self.stock <= 10

    @property
    def valor_inventario(self):
        return self.precio * self.stock if self.precio is not None else Decimal('0')
