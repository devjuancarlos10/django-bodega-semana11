from django.contrib import admin

from .models import Producto


# Registro basico; se ampliara en la Semana 12 (admin, formularios, sesiones).
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'disponible', 'fecha_registro')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre',)
