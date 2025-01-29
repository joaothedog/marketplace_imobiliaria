from rest_framework import viewsets
from .models import Imobiliaria, Imovel, Imagem, PacoteAnuncio, Contrato
from .serializers import ImobiliariaSerializer, ImovelSerializer, ImagemSerializer, PacoteAnuncioSerializer, ContratoSerializer

class ImobiliariaViewSet(viewsets.ModelViewSet):
    queryset = Imobiliaria.objects.all()
    serializer_class = ImobiliariaSerializer

class ImovelViewSet(viewsets.ModelViewSet):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer

class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer

class PacoteAnuncioViewSet(viewsets.ModelViewSet):
    queryset = PacoteAnuncio.objects.all()
    serializer_class = PacoteAnuncioSerializer

class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer