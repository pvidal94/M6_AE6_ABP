from django.db import models

class Product(models.Model):
    name = models.CharField(
        max_length=200, 
        verbose_name='Nombre del Producto',
        help_text='Nombre comercial del producto.'
    )
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción detallada del producto.'
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Precio de Venta'
    )
    stock = models.IntegerField(
        verbose_name='Stock Disponible',
        help_text='Número de unidades en almacén.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Fecha de Creación'
    )

    class Meta:
        verbose_name = 'Producto'