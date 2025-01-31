from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import ImobiliariaUser, NormalUser, Imovel, Oferta

# Obtenha o modelo de usuário personalizado
User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        # URLs para os endpoints
        self.register_imobiliaria_url = reverse('register-imobiliaria')
        self.register_normal_user_url = reverse('register-normal-user')
        self.login_url = reverse('login')
        self.imoveis_url = reverse('imovel-list')
        self.ofertas_url = reverse('oferta-list')

    def test_registro_imobiliaria(self):
        """
        Testa o registro de uma nova imobiliária.
        """
        data = {
            "user": {
                "username": "imobiliaria1",
                "password": "senha123",
                "tipo_usuario": "IMOBILIARIA"
            },
            "nome": "Imobiliária Teste",
            "email": "imobiliaria@teste.com",
            "telefone": "123456789",
            "whatsapp": "987654321",
            "endereco": "Rua Teste, 123"
        }

        response = self.client.post(self.register_imobiliaria_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ImobiliariaUser.objects.count(), 1)
        self.assertEqual(ImobiliariaUser.objects.get().nome, "Imobiliária Teste")

    def test_registro_normal_user(self):
        """
        Testa o registro de um novo usuário normal.
        """
        data = {
            "user": {
                "username": "usuario1",
                "password": "senha123",
                "tipo_usuario": "NORMAL"
            },
            "nome": "Usuário Teste",
            "email": "usuario@teste.com",
            "telefone": "123456789"
        }

        response = self.client.post(self.register_normal_user_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NormalUser.objects.count(), 1)
        self.assertEqual(NormalUser.objects.get().nome, "Usuário Teste")

    def test_login(self):
        """
        Testa o login e verifica se os tokens são retornados.
        """
        # Primeiro, registre um usuário
        user_data = {
            "user": {
                "username": "imobiliaria1",
                "password": "senha123",
                "tipo_usuario": "IMOBILIARIA"
            },
            "nome": "Imobiliária Teste",
            "email": "imobiliaria@teste.com",
            "telefone": "123456789",
            "whatsapp": "987654321",
            "endereco": "Rua Teste, 123"
        }
        self.client.post(self.register_imobiliaria_url, user_data, format='json')

        # Agora, faça o login
        login_data = {
            "username": "imobiliaria1",
            "password": "senha123"
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertEqual(response.data['user_type'], 'IMOBILIARIA')

    def test_acesso_protegido(self):
        """
        Testa se a criação de imóveis é protegida, mas a listagem é pública.
        """
        # Tente acessar a listagem de imóveis sem token (deve ser público)
        response = self.client.get(self.imoveis_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Tente criar um imóvel sem token (deve ser protegido)
        imovel_data = {
            "titulo": "Casa Teste",
            "descricao": "Descrição Teste",
            "endereco": "Rua Teste, 123",
            "bairro": "Centro",
            "preco_venda": 500000,
            "preco_locacao": 2000,
            "destaque": True,
            "imobiliaria": 1  # ID da imobiliária (deve existir no banco de dados)
        }
        response = self.client.post(self.imoveis_url, imovel_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Agora, faça o login e tente criar um imóvel com token
        user_data = {
            "user": {
                "username": "imobiliaria1",
                "password": "senha123",
                "tipo_usuario": "IMOBILIARIA"
            },
            "nome": "Imobiliária Teste",
            "email": "imobiliaria@teste.com",
            "telefone": "123456789",
            "whatsapp": "987654321",
            "endereco": "Rua Teste, 123"
        }
        self.client.post(self.register_imobiliaria_url, user_data, format='json')

        login_data = {
            "username": "imobiliaria1",
            "password": "senha123"
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.imoveis_url, imovel_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class OfertaTests(APITestCase):
    def setUp(self):
        self.ofertas_url = reverse('oferta-list')
        self.user_data = {
            "user": {
                "username": "usuario1",
                "password": "senha123",
                "tipo_usuario": "NORMAL"
            },
            "nome": "Usuário Teste",
            "email": "usuario@teste.com",
            "telefone": "123456789"
        }
        self.client.post(reverse('register-normal-user'), self.user_data, format='json')

        # Faça o login para obter o token
        login_data = {
            "username": "usuario1",
            "password": "senha123"
        }
        self.login_response = self.client.post(reverse('login'), login_data, format='json')
        self.access_token = self.login_response.data['access']

    def test_criar_oferta_autenticado(self):
        """
        Testa se um usuário normal autenticado pode criar uma oferta.
        """
        # Crie uma imobiliária
        imobiliaria_data = {
            "user": {
                "username": "imobiliaria1",
                "password": "senha123",
                "tipo_usuario": "IMOBILIARIA"
            },
            "nome": "Imobiliária Teste",
            "email": "imobiliaria@teste.com",
            "telefone": "123456789",
            "whatsapp": "987654321",
            "endereco": "Rua Teste, 123"
        }
        self.client.post(self.register_imobiliaria_url, imobiliaria_data, format='json')

        # Crie um imóvel associado à imobiliária
        imovel_data = {
            "titulo": "Casa Teste",
            "descricao": "Descrição Teste",
            "endereco": "Rua Teste, 123",
            "bairro": "Centro",
            "preco_venda": 500000,
            "preco_locacao": 2000,
            "destaque": True,
            "imobiliaria": 1  # ID da imobiliária criada acima
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        imovel_response = self.client.post(self.imoveis_url, imovel_data, format='json')
        self.assertEqual(imovel_response.status_code, status.HTTP_201_CREATED)  # Verifique se o imóvel foi criado
        imovel_id = imovel_response.data['id']  # Agora o 'id' deve estar presente

        # Crie uma oferta
        oferta_data = {
            "imovel": imovel_id,
            "valor": 450000,
            "tipo": "COMPRA"
        }
        response = self.client.post(self.ofertas_url, oferta_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verifique se a oferta foi associada ao usuário correto
        oferta = Oferta.objects.get(id=response.data['id'])
        self.assertEqual(oferta.usuario.username, "usuario1")

    def test_criar_oferta_imobiliaria(self):
        """
        Testa se uma imobiliária não pode criar uma oferta.
        """
        # Crie uma imobiliária
        imobiliaria_data = {
            "user": {
                "username": "imobiliaria1",
                "password": "senha123",
                "tipo_usuario": "IMOBILIARIA"
            },
            "nome": "Imobiliária Teste",
            "email": "imobiliaria@teste.com",
            "telefone": "123456789",
            "whatsapp": "987654321",
            "endereco": "Rua Teste, 123"
        }
        self.client.post(self.register_imobiliaria_url, imobiliaria_data, format='json')

        # Faça o login como imobiliária
        login_data = {
            "username": "imobiliaria1",
            "password": "senha123"
        }
        login_response = self.client.post(self.login_url, login_data, format='json')
        access_token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        # Crie um imóvel associado à imobiliária
        imovel_data = {
            "titulo": "Casa Teste",
            "descricao": "Descrição Teste",
            "endereco": "Rua Teste, 123",
            "bairro": "Centro",
            "preco_venda": 500000,
            "preco_locacao": 2000,
            "destaque": True,
            "imobiliaria": 1  # ID da imobiliária criada acima
        }
        imovel_response = self.client.post(self.imoveis_url, imovel_data, format='json')
        self.assertEqual(imovel_response.status_code, status.HTTP_201_CREATED)  # Verifique se o imóvel foi criado
        imovel_id = imovel_response.data['id']  # Agora o 'id' deve estar presente

        # Tente criar uma oferta (deve falhar)
        oferta_data = {
            "imovel": imovel_id,
            "valor": 450000,
            "tipo": "COMPRA"
        }
        response = self.client.post(self.ofertas_url, oferta_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Proibido para imobiliárias