from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .filters import ImovelFilter
from django_filters import rest_framework as filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .serializers import ImobiliariaUserSerializer, NormalUserSerializer, LoginSerializer, ImobiliariaSerializer, ImovelSerializer, ImagemSerializer, PacoteAnuncioSerializer, ContratoSerializer

from .models import Imobiliaria, Imovel, Imagem, PacoteAnuncio, Contrato

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

class RegisterImobiliariaView(generics.CreateAPIView):
    serializer_class = ImobiliariaUserSerializer
    permission_classes = [permissions.AllowAny]

class RegisterNormalUserView(generics.CreateAPIView):
    serializer_class = NormalUserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_type': user.tipo_usuario  # Retorna o tipo de usuário
        })
    
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