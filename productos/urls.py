from django.urls import path

from . import views

# app_name crea un espacio de nombres: en las plantillas se usa
# {% url 'productos:catalogo' %} en lugar de escribir "/catalogo/".
app_name = 'productos'

urlpatterns = [
    path('', views.home, name='home'),                                   # FBV
    path('catalogo/', views.ProductoListView.as_view(), name='catalogo'),  # CBV
    path('producto/<int:pk>/', views.ProductoDetailView.as_view(), name='detalle'),
]
