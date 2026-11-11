from django.db.models import Count, Sum
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Producto


# ---------------------------------------------------------------------------
# FBV (Function-Based View): recibe un HttpRequest y devuelve un HttpResponse.
# render() carga la plantilla, le inyecta el contexto y arma la respuesta.
# ---------------------------------------------------------------------------
def home(request):
    productos = Producto.objects.all()  # QuerySet lazy: aun no hay SQL
    contexto = {
        'titulo': 'bienvenido a la bodega don lucho',
        'total_productos': productos.count(),
        'total_unidades': productos.aggregate(total=Sum('stock'))['total'] or 0,
        'destacados': productos.disponibles().order_by('-fecha_registro')[:4],
        'alertas_stock': productos.stock_bajo(),
    }
    return render(request, 'productos/home.html', contexto)


# ---------------------------------------------------------------------------
# CBV (Class-Based View): ListView ya implementa GET -> get_queryset() ->
# get_context_data() -> render. Solo personalizamos lo necesario.
# El QuerySet se expone en la plantilla como 'object_list' y como
# 'productos' (context_object_name).
# ---------------------------------------------------------------------------
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/catalogo.html'
    context_object_name = 'productos'
    paginate_by = 8

    def get_queryset(self):
        categoria = self.request.GET.get('categoria', '')
        texto = self.request.GET.get('q', '').strip()
        return Producto.objects.por_categoria(categoria).buscar(texto)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Producto.Categoria.choices
        context['categoria_actual'] = self.request.GET.get('categoria', '')
        context['busqueda'] = self.request.GET.get('q', '')
        etiquetas = dict(Producto.Categoria.choices)
        conteo = (
            Producto.objects.values('categoria')
            .annotate(cantidad=Count('id'))
            .order_by('categoria')
        )
        context['resumen_categorias'] = [
            {'nombre': etiquetas[fila['categoria']], 'cantidad': fila['cantidad']}
            for fila in conteo
        ]
        return context


class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/detalle.html'
    context_object_name = 'producto'
