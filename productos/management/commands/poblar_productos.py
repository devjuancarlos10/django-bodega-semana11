from decimal import Decimal

from django.core.management.base import BaseCommand

from productos.models import Producto

C = Producto.Categoria

PRODUCTOS = [
    # nombre, categoria, precio, stock, descripcion
    ('arroz costeño 5 kg', C.ABARROTES, '22.50', 40, 'Arroz extra graneado, bolsa de 5 kilogramos.'),
    ('azucar rubia 1 kg', C.ABARROTES, '4.20', 8, 'Azucar rubia de cana, bolsa de 1 kilogramo.'),
    ('aceite primor 1 l', C.ABARROTES, '9.90', 25, 'Aceite vegetal en botella de 1 litro.'),
    ('fideo spaghetti don vittorio', C.ABARROTES, '3.80', 60, 'Paquete de 500 gramos.'),
    ('atun florida en trozos', C.ABARROTES, '6.50', 5, 'Lata de 170 gramos en aceite vegetal.'),
    ('inca kola 1.5 l', C.BEBIDAS, '7.50', 30, 'Gaseosa en botella descartable de 1.5 litros.'),
    ('agua cielo 625 ml', C.BEBIDAS, '1.50', 100, 'Agua de mesa sin gas.'),
    ('chicha morada gloria 1 l', C.BEBIDAS, '5.20', 0, 'Bebida a base de maiz morado.'),
    ('leche gloria tarro azul', C.LACTEOS, '4.10', 48, 'Leche evaporada entera, 400 gramos.'),
    ('yogurt laive fresa 1 kg', C.LACTEOS, '7.80', 9, 'Yogurt bebible sabor fresa.'),
    ('queso andino 500 g', C.LACTEOS, '15.00', 12, 'Queso fresco de la sierra central.'),
    ('detergente bolivar 750 g', C.LIMPIEZA, '11.90', 18, 'Detergente en polvo para ropa.'),
    ('lejia clorox 1 l', C.LIMPIEZA, '4.50', 22, 'Lejia tradicional.'),
    ('papel higienico suave x4', C.LIMPIEZA, '6.90', 3, 'Paquete de 4 rollos doble hoja.'),
    ('galletas soda field', C.SNACKS, '1.00', 80, 'Paquete individual de galletas de soda.'),
    ('chocolate sublime', C.SNACKS, '2.00', 45, 'Chocolate con mani.'),
    ('papas lays clasicas', C.SNACKS, '2.50', 7, 'Bolsa de 42 gramos.'),
]


class Command(BaseCommand):
    help = 'Puebla la tabla Producto con datos de ejemplo usando el ORM (sin tocar SQLite a mano).'

    def add_arguments(self, parser):
        parser.add_argument('--limpiar', action='store_true', help='Borra los productos antes de poblar.')

    def handle(self, *args, **options):
        if options['limpiar']:
            borrados, _ = Producto.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Se eliminaron {borrados} productos.'))

        creados = 0
        for nombre, categoria, precio, stock, descripcion in PRODUCTOS:
            _, nuevo = Producto.objects.get_or_create(
                nombre=nombre,
                defaults={
                    'categoria': categoria,
                    'precio': Decimal(precio),
                    'stock': stock,
                    'disponible': stock > 0,
                    'descripcion': descripcion,
                },
            )
            creados += int(nuevo)

        self.stdout.write(self.style.SUCCESS(
            f'Listo: {creados} productos nuevos. Total en BD: {Producto.objects.count()}.'
        ))
