import django_filters
from .models import Imovel

class ImovelFilter(django_filters.FilterSet):
    preco_venda_min = django_filters.NumberFilter(field_name="preco_venda", lookup_expr='gte')
    preco_venda_max = django_filters.NumberFilter(field_name="preco_venda", lookup_expr='lte')
    preco_locacao_min = django_filters.NumberFilter(field_name="preco_locacao", lookup_expr='gte')
    preco_locacao_max = django_filters.NumberFilter(field_name="preco_locacao", lookup_expr='lte')
    bairro = django_filters.CharFilter(field_name="bairro", lookup_expr='icontains')
    destaque = django_filters.BooleanFilter(field_name="destaque")

    class Meta:
        model = Imovel
        fields = [
            'preco_venda_min', 'preco_venda_max',
            'preco_locacao_min', 'preco_locacao_max',
            'bairro', 'destaque'
        ]