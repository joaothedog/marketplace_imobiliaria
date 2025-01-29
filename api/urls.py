from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImobiliariaViewSet, ImovelViewSet, ImagemViewSet, PacoteAnuncioViewSet, ContratoViewSet

router = DefaultRouter()
router.register(r'imobiliarias', ImobiliariaViewSet)
router.register(r'imoveis', ImovelViewSet)
router.register(r'imagens', ImagemViewSet)
router.register(r'pacotes', PacoteAnuncioViewSet)
router.register(r'contratos', ContratoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]