from django.shortcuts import render
import django_tables2 as tables
from django_tables2.columns.linkcolumn import LinkColumn
from .models import Transaccion


class TablaTransaccion(tables.Table):
    BotonEliminar = tables.TemplateColumn(
        '''<a href="">Eliminar producto</a>''',
        verbose_name = 'BotonEliminar')
    class Meta:
        model = Transaccion
        fields = (
            'BotonEliminar',
        )
    
    def render_compra(self, value):
        return"<%s>" % value

