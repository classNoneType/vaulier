from django.shortcuts import render
from django.views import generic
from .models import Producto, Transaccion
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .serializers import ProductoSerializer
from django.http import HttpResponse
import django_tables2 as tables


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get_queryset(self):
        Productos = Producto.objects.all()
        id = self.request.GET.get('')
        if id:
            # __contains >> LIKE en sql
            Productos = Productos.filter(id__contains = id)
        return Productos



def CatalogoVinilo(request):
    productos = Producto.objects.filter(FechaPublicacion__lte = timezone.now()).order_by('FechaPublicacion')
    return render(request, 'vaulier/index.html', {'productos' : productos})

def DetalleVinilo(request, pk):
    productos = get_object_or_404(Producto, pk = pk)
    return render(request, 'vaulier/detail.html', {'productos': productos})



class TransaccionListView(tables.SingleTableView):
    model = Producto
    table_class = Transaccion
    template_name='vaulier/transaccion.html'

def TransaccionProducto(request, pk):
    transaccion = get_object_or_404(Transaccion, pk = pk)
    return render(request, 'vaulier/transaccion.html', {'transaccion' : transaccion})