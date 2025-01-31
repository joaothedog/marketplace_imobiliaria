from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ImobiliariaViewSet,
    ImovelViewSet,
    ImagemViewSet,
    PacoteAnuncioViewSet,
    ContratoViewSet,
    RegisterImobiliariaView,
    RegisterNormalUserView,
    LoginView,
)

router = DefaultRouter()
router.register(r"imobiliarias", ImobiliariaViewSet)
router.register(r"imoveis", ImovelViewSet)
router.register(r"imagens", ImagemViewSet)
router.register(r"pacotes", PacoteAnuncioViewSet)
router.register(r"contratos", ContratoViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "register/imobiliaria/",
        RegisterImobiliariaView.as_view(),
        name="register-imobiliaria",
    ),
    path(
        "register/normal-user/",
        RegisterNormalUserView.as_view(),
        name="register-normal-user",
    ),
    path("login/", LoginView.as_view(), name="login"),
]
