
from django.db import models
from django.utils import timezone

class Producto(models.Model):
    AutorPublicacion = models.ForeignKey('auth.User', on_delete = models.CASCADE)

    ArtistaProducto = models.CharField(max_length = 50, verbose_name = 'Artista')
    AlbumProducto = models.CharField(max_length = 50, verbose_name = 'Album')
    ImagenProducto = models.TextField(max_length = 30, verbose_name = 'Imagen')
    PrecioProducto = models.CharField(max_length = 15, verbose_name = 'Precio')
    CodigoProducto = models.TextField(max_length = 50, verbose_name = 'Codigo Spotify')
    StockProducto = models.IntegerField(default = 0, verbose_name = 'Stock')

    FechaCreacion = models.DateTimeField(default = timezone.now)
    FechaPublicacion = models.DateTimeField(blank = True, null = True)

    def publish(self):
        self.FechaPublicacion = timezone.now()
        self.save()

    def __str__(self):
        return self.AlbumProducto

class CarroCompra(models.Model):
    ProductoID = models.ForeignKey(Producto, on_delete=models.CASCADE)
    ImagenProducto = models.TextField(max_length = 30, verbose_name = 'Imagen')
    ArtistaProducto = models.CharField(max_length = 50, verbose_name = 'Artista')
    AlbumProducto = models.CharField(max_length = 50, verbose_name = 'Album')
    CantidadProducto = models.IntegerField(default = 0, verbose_name = 'Cantidad')
    def __str__(self):
        return self.ProductoID

class Transaccion(models.Model):
    ProductoID = models.ForeignKey(Producto, on_delete=models.CASCADE)
    PrecioProducto = models.CharField(max_length = 15, verbose_name = 'Precio')
    TotalTransaccion = models.IntegerField(default = 0, verbose_name = 'Total')
    FechaTransaccion = models.DateTimeField(default = timezone.now)
    def __str__(self):
        return self.ProductoID