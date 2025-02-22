from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView )
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Marketplace de Imóveis API",
        default_version='v1',               
        description="API para gerenciamento de imóveis e imobiliárias.",
        contact=openapi.Contact(email="jvcbatist4@outlook.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Permissões para acessar a documentação
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obatin_pair'), # p/ realizar o login
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'), # refresh do tk
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

