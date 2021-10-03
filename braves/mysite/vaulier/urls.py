from django.urls import path, include
from .views import CatalogoVinilo, DetalleVinilo, ProductoViewSet, TransaccionProducto
from rest_framework import routers

router = routers.DefaultRouter()
router.register('producto', ProductoViewSet)

urlpatterns = [
    path('', CatalogoVinilo, name = 'index'),
    path('vinilo/<int:pk>/', DetalleVinilo, name = 'detail'),
    path('api/', include(router.urls)),
    path('transaccion/<int:pk>/', TransaccionProducto, name='transaccion'),
]