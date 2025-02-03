from rest_framework import viewsets, permissions, generics, status
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .filters import ImovelFilter
from django_filters import rest_framework as filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    ImobiliariaUserSerializer,
    NormalUserSerializer,
    LoginSerializer,
    OfertaSerializer,
    ImobiliariaSerializer,
    ImovelSerializer,
    ImagemSerializer,
    PacoteAnuncioSerializer,
    ContratoSerializer,
)

from .models import Imobiliaria, Imovel, Imagem, PacoteAnuncio, Contrato, Oferta


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class RegisterImobiliariaView(generics.CreateAPIView):
    serializer_class = ImobiliariaUserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Registra uma nova imobiliária no sistema.",
        request_body=ImobiliariaUserSerializer,
        responses={
            201: "Imobiliária registrada com sucesso.",
            400: "Dados inválidos.",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterNormalUserView(generics.CreateAPIView):
    serializer_class = NormalUserSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Registra um novo usuário normal no sistema.",
        request_body=NormalUserSerializer,
        responses={
            201: "Usuário registrado com sucesso.",
            400: "Dados inválidos.",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Realiza o login de um usuário e retorna tokens JWT.",
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login realizado com sucesso.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                        "access": openapi.Schema(type=openapi.TYPE_STRING),
                        "user_type": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: "Credenciais inválidas.",
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_type": user.tipo_usuario,
            }
        )


class ImobiliariaViewSet(viewsets.ModelViewSet):
    queryset = Imobiliaria.objects.all()
    serializer_class = ImobiliariaSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Lista todas as imobiliárias.",
        responses={200: ImobiliariaSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retorna os detalhes de uma imobiliária específica.",
        responses={200: ImobiliariaSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria uma nova imobiliária.",
        request_body=ImobiliariaSerializer,
        responses={201: ImobiliariaSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualiza uma imobiliária existente.",
        request_body=ImobiliariaSerializer,
        responses={200: ImobiliariaSerializer()},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Exclui uma imobiliária.",
        responses={204: "Imobiliária excluída com sucesso."},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class ImovelViewSet(viewsets.ModelViewSet):
    queryset = Imovel.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ImovelSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ImovelFilter

    @swagger_auto_schema(
        operation_description="Lista todos os imóveis, com opção de filtragem.",
        manual_parameters=[
            openapi.Parameter(
                name="bairro",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filtrar imóveis por bairro.",
            ),
            openapi.Parameter(
                name="preco_venda_min",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                description="Filtrar imóveis por preço de venda mínimo.",
            ),
            openapi.Parameter(
                name="preco_venda_max",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                description="Filtrar imóveis por preço de venda máximo.",
            ),
        ],
        responses={200: ImovelSerializer(many=True)},
    )
    @method_decorator(cache_page(60 * 15))  # 15min cache
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retorna os detalhes de um imóvel específico.",
        responses={200: ImovelSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria um novo imóvel.",
        request_body=ImovelSerializer,
        responses={201: ImovelSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualiza um imóvel existente.",
        request_body=ImovelSerializer,
        responses={200: ImovelSerializer()},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Exclui um imóvel.",
        responses={204: "Imóvel excluído com sucesso."},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class OfertaViewSet(viewsets.ModelViewSet):
    queryset = Oferta.objects.all()
    serializer_class = OfertaSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Lista todas as ofertas do usuário autenticado.",
        responses={200: OfertaSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria uma nova oferta.",
        request_body=OfertaSerializer,
        responses={201: OfertaSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ImagemViewSet(viewsets.ModelViewSet):
    queryset = Imagem.objects.all()
    serializer_class = ImagemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_description="Lista todas as imagens.",
        responses={200: ImagemSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria uma nova imagem.",
        request_body=ImagemSerializer,
        responses={201: ImagemSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class PacoteAnuncioViewSet(viewsets.ModelViewSet):
    queryset = PacoteAnuncio.objects.all()
    serializer_class = PacoteAnuncioSerializer

    @swagger_auto_schema(
        operation_description="Lista todos os pacotes de anúncios.",
        responses={200: PacoteAnuncioSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria um novo pacote de anúncios.",
        request_body=PacoteAnuncioSerializer,
        responses={201: PacoteAnuncioSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ContratoViewSet(viewsets.ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer

    @swagger_auto_schema(
        operation_description="Lista todos os contratos.",
        responses={200: ContratoSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Cria um novo contrato.",
        request_body=ContratoSerializer,
        responses={201: ContratoSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)