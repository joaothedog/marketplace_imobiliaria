from rest_framework import viewsets
from .models import Imobiliaria, Imovel, Imagem, PacoteAnuncio, Contrato
from .serializers import ImobiliariaSerializer, ImovelSerializer, ImagemSerializer, PacoteAnuncioSerializer, ContratoSerializer
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ImobiliariaViewSet(viewsets.ModelViewSet):
    queryset = Imobiliaria.objects.all()
    serializer_class = ImobiliariaSerializer

class ImovelViewSet(viewsets.ModelViewSet):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer

class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PacoteAnuncioViewSet(viewsets.ModelViewSet):
    queryset = PacoteAnuncio.objects.all()
    serializer_class = PacoteAnuncioSerializer
    
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer