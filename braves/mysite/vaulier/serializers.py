from .models import Producto
from rest_framework import serializers

class ProductoSerializer(serializers.ModelSerializer):

    AutorPublicacion = serializers.CharField(max_length = 50)
    ArtistaProducto = serializers.CharField(max_length = 50)
    AlbumProducto = serializers.CharField(max_length = 50)
    ImagenProducto = serializers.CharField(max_length = 50)
    PrecioProducto = serializers.CharField(max_length = 50)
    CodigoProducto = serializers.CharField(max_length = 50)
    StockProducto = serializers.IntegerField(default = 0)
    FechaPublicacion = serializers.DateTimeField()

    def ValidacionProducto(self, value):
        Validacion = Producto.objects.filter(AlbumProducto = value).exists()
        if Validacion:
            raise serializers.ValidationError('[ * ] Este vinilo ya existe')
        return value
    class Meta:
        model = Producto
        fields = '__all__'
        