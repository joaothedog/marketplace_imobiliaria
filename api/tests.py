from django.test import TestCase
from .models import Imobiliaria, Imovel, UserProfile, User
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .serializers import UserRegisterSerializer
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class APITests(APITestCase):
    def setUp(self):
        """Configuração inicial para os testes."""
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123"
        )
        self.imobiliaria = Imobiliaria.objects.create(
            nome="Imobiliária Teste",
            email="teste@imobiliaria.com",
            telefone="123456789",
            endereco="Rua Teste, 123"
        )
        self.imovel = Imovel.objects.create(
            titulo="Casa Teste",
            descricao="Descrição teste",
            endereco="Rua Teste, 456",
            bairro="Bairro Teste",
            preco_venda=500000,
            imobiliaria=self.imobiliaria
        )

    def test_list_imoveis(self):
        """Testa o endpoint de listagem de imóveis."""
        url = reverse('imovel-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_imovel_authenticated(self):
        """Testa a criação de um imóvel com autenticação."""
        self.client.force_authenticate(user=self.user)
        url = reverse('imovel-list')
        data = {
            "titulo": "Nova Casa",
            "descricao": "Descrição da nova casa",
            "endereco": "Rua Nova, 789",
            "bairro": "Bairro Novo",
            "preco_venda": 600000,
            "imobiliaria": self.imobiliaria.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Imovel.objects.count(), 2)

    def test_create_imovel_unauthenticated(self):
        """Testa a criação de um imóvel sem autenticação."""
        url = reverse('imovel-list')
        data = {
            "titulo": "Nova Casa",
            "descricao": "Descrição da nova casa",
            "endereco": "Rua Nova, 789",
            "bairro": "Bairro Novo",
            "preco_venda": 600000,
            "imobiliaria": self.imobiliaria.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class SerializerTests(APITestCase):
    def test_user_register_serializer(self):
        """Testa o serializer de registro de usuário."""
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
            "password2": "testpass123",
            "full_name": "Usuário Teste",
            "phone": "987654321",
            "is_imobiliaria": False
        }
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@example.com")

class ModelTests(TestCase):
    def test_create_imobiliaria(self):
        """Testa a criação de uma imobiliária."""
        imobiliaria = Imobiliaria.objects.create(
            nome="Imobiliária Teste",
            email="teste@imobiliaria.com",
            telefone="123456789",
            endereco="Rua Teste, 123"
        )
        self.assertEqual(imobiliaria.nome, "Imobiliária Teste")

    def test_create_imovel(self):
        """Testa a criação de um imóvel."""
        imobiliaria = Imobiliaria.objects.create(
            nome="Imobiliária Teste",
            email="teste@imobiliaria.com",
            telefone="123456789",
            endereco="Rua Teste, 123"
        )
        imovel = Imovel.objects.create(
            titulo="Casa Teste",
            descricao="Descrição teste",
            endereco="Rua Teste, 456",
            bairro="Bairro Teste",
            preco_venda=500000,
            imobiliaria=imobiliaria
        )
        self.assertEqual(imovel.titulo, "Casa Teste")
        self.assertEqual(imovel.imobiliaria.nome, "Imobiliária Teste")

    def test_create_user_profile(self):
        """Testa a criação de um perfil de usuário."""
        user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123"
        )
        profile = UserProfile.objects.create(
            user=user,
            full_name="Usuário Teste",
            phone="987654321",
            is_imobiliaria=False
        )
        self.assertEqual(profile.user.username, "testuser")
        self.assertEqual(profile.full_name, "Usuário Teste")