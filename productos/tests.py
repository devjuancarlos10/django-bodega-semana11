from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Producto


class ProductoModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.arroz = Producto.objects.create(
            nombre='arroz', categoria=Producto.Categoria.ABARROTES,
            precio=Decimal('22.50'), stock=40,
        )
        cls.atun = Producto.objects.create(
            nombre='atun', categoria=Producto.Categoria.ABARROTES,
            precio=Decimal('6.50'), stock=5,
        )
        cls.chicha = Producto.objects.create(
            nombre='chicha', categoria=Producto.Categoria.BEBIDAS,
            precio=Decimal('5.20'), stock=0, disponible=False,
        )

    def test_str(self):
        self.assertEqual(str(self.arroz), 'arroz (S/ 22.50)')

    def test_queryset_disponibles_y_filtros(self):
        self.assertEqual(Producto.objects.count(), 3)
        self.assertNotIn(self.chicha, Producto.objects.disponibles())
        self.assertEqual(Producto.objects.por_categoria('BEB').count(), 1)
        self.assertQuerySetEqual(Producto.objects.stock_bajo(), [self.atun, self.chicha], ordered=False)

    def test_valor_inventario(self):
        self.assertEqual(self.arroz.valor_inventario, Decimal('900.00'))


class VistasTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Producto.objects.create(nombre='leche gloria', categoria='LAC', precio=Decimal('4.10'), stock=48)

    def test_home_fbv(self):
        resp = self.client.get(reverse('productos:home'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'productos/home.html')
        self.assertTemplateUsed(resp, 'productos/base.html')
        self.assertContains(resp, 'Bienvenido A La Bodega Don Lucho')  # filtro |title

    def test_catalogo_cbv_contexto(self):
        resp = self.client.get(reverse('productos:catalogo'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('object_list', resp.context)
        self.assertIn('productos', resp.context)
        self.assertIn('categorias', resp.context)  # agregado en get_context_data
        self.assertContains(resp, 'Leche Gloria')

    def test_catalogo_filtra_por_categoria(self):
        resp = self.client.get(reverse('productos:catalogo'), {'categoria': 'BEB'})
        self.assertEqual(len(resp.context['productos']), 0)

    def test_detalle_y_404(self):
        p = Producto.objects.get()
        self.assertEqual(self.client.get(p.get_absolute_url()).status_code, 200)
        self.assertEqual(self.client.get(reverse('productos:detalle', args=[999])).status_code, 404)
