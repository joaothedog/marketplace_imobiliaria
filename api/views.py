from rest_framework import viewsets, permissions, generics
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .filters import ImovelFilter
from django_filters import rest_framework as filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django.contrib.auth.models import User

from .models import Imobiliaria, Imovel, Imagem, PacoteAnuncio, Contrato
from .serializers import ImobiliariaSerializer, ImovelSerializer, ImagemSerializer, PacoteAnuncioSerializer, ContratoSerializer, UserRegisterSerializer

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]  # Permite que qualquer pessoa se registre
    
class ImobiliariaViewSet(viewsets.ModelViewSet):
    queryset = Imobiliaria.objects.all()
    serializer_class = ImobiliariaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ImovelViewSet(viewsets.ModelViewSet):
    queryset = Imovel.objects.all()
    serializer_class = ImovelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ImovelFilter
    
    @method_decorator(cache_page(60 * 15))  # 15min cache
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

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