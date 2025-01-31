# API Marketplace de Imóveis

Esta é uma API Django Rest Framework (DRF) para um marketplace de imóveis, onde imobiliárias podem anunciar imóveis para venda ou locação. A API permite a listagem de imóveis, criação de novos anúncios (com autenticação JWT), registro de usuários e muito mais.

## Tecnologias Utilizadas
- Python: Linguagem de programação principal.
- Django: Framework web para desenvolvimento rápido e seguro.
- Django Rest Framework (DRF): Framework para construção de APIs RESTful.
- Simple JWT: Biblioteca para autenticação via JSON Web Tokens (JWT).
- SQLite: Banco de dados padrão para desenvolvimento.
- Postman/Insomnia: Ferramentas para testar os endpoints da API.

## Funcionalidades da API
- Listagem de Imóveis: Qualquer usuário pode visualizar a lista de imóveis disponíveis.
- Criação de Imóveis: Apenas usuários autenticados podem criar novos anúncios de imóveis.
- Autenticação JWT: Sistema de autenticação seguro usando JSON Web Tokens.
- Registro de Usuários: Endpoint para registro de novos usuários.
- Filtros de Busca: Filtragem de imóveis por bairro, preço e tipo (venda/locação). (EM CONSTRUÇÃO)

## Passo a Passo para Utilizar a API

### 1. Clonar o Repositório
```sh
git clone https://github.com/joaothedog/marketplace_imobiliaria.git
```

### 2. Criar e Ativar um Ambiente Virtual
```sh
python -m venv venv
source venv/bin/activate  # Se você estiver no Windows, utilize: venv\Scripts\activate
```

### 3. Instalar Dependências
```sh
pip install -r requirements.txt
```

### 4. Configurar o Banco de Dados
```sh
python manage.py migrate
```

### 5. Rodar o Servidor
```sh
python manage.py runserver
```

### 6. Rodar os testes automatizados
```sh
python manage.py test
```

A API estará disponível em `http://127.0.0.1:8000/api/`.

## Endpoints

### Imobiliárias
- **GET /imobiliarias/** - Listar todas as imobiliárias.
- **POST /imobiliarias/** - Criar uma nova imobiliária. (AUTH)
- **GET /imobiliarias/{id}/** - Detalhes de uma imobiliária.
- **PUT /imobiliarias/{id}/** - Atualizar uma imobiliária.
- **DELETE /imobiliarias/{id}/** - Excluir uma imobiliária.

### Imóveis
- **GET /imoveis/** - Listar todos os imóveis (com filtros: bairro, preço, tipo).
- **POST /imoveis/** - Criar um novo imóvel. (AUTH)
- **GET /imoveis/{id}/** - Detalhes de um imóvel.
- **PUT /imoveis/{id}/** - Atualizar um imóvel.
- **DELETE /imoveis/{id}/** - Excluir um imóvel.

### Imagens
- **POST /imoveis/{id}/imagens/** - Adicionar imagem a um imóvel.
- **DELETE /imagens/{id}/** - Excluir uma imagem.

### Pacotes de Anúncios
- **GET /pacotes/** - Listar todos os pacotes.
- **POST /pacotes/** - Criar um novo pacote. (AUTH)
- **GET /pacotes/{id}/** - Detalhes de um pacote.
- **PUT /pacotes/{id}/** - Atualizar um pacote.
- **DELETE /pacotes/{id}/** - Excluir um pacote.

### Contratos
- **GET /contratos/** - Listar todos os contratos.
- **POST /contratos/** - Criar um novo contrato. (AUTH)
- **GET /contratos/{id}/** - Detalhes de um contrato.
- **PUT /contratos/{id}/** - Atualizar um contrato.
- **DELETE /contratos/{id}/** - Excluir um contrato.

### Registrar usuário ou imobiliária
- **POST /api/register/imobiliaria/**
- **Body:**
```json
{
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
```
- **Resposta:**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "imobiliaria1",
    "tipo_usuario": "IMOBILIARIA"
  },
  "nome": "Imobiliária Teste",
  "email": "imobiliaria@teste.com",
  "telefone": "123456789",
  "whatsapp": "987654321",
  "endereco": "Rua Teste, 123"
}
```

- **POST /api/register/normal-user/**
- **Body:**
```json
{
  "user": {
    "username": "usuario1",
    "password": "senha123",
    "tipo_usuario": "NORMAL"
  },
  "nome": "Usuário Teste",
  "email": "usuario@teste.com",
  "telefone": "123456789"
}
```
- **Resposta:**
```json
{
  "id": 1,
  "user": {
    "id": 2,
    "username": "usuario1",
    "tipo_usuario": "NORMAL"
  },
  "nome": "Usuário Teste",
  "email": "usuario@teste.com",
  "telefone": "123456789"
}
```

- **POST /api/login**
- **Body:**
```json
{
  "username": "imobiliaria1",
  "password": "senha123"
}
```
- **Resposta:**
```json
{
  "refresh": "token_de_refresh",
  "access": "token_de_acesso",
  "user_type": "IMOBILIARIA"
}
```

### Autenticação JWT

Agora, crie um superuser do Django com:

```sh
python manage.py createsuperuser # Para lidar com a autenticação é necessário criar o usuario
```

e utilize o Postman ou Insomnia (utilizei o Postman, por costume, mas fica à seu critério) para realizar as requisições:

#### Obter Token de Acesso
- **Endpoint:** `POST /api/token/`
- **Body:**
```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```
- **Resposta:**
```json
{
  "refresh": "refresh_token_aqui",
  "access": "access_token_aqui"
}
```

#### Atualizar Token de Acesso
- **Endpoint:** `POST /api/token/refresh/`
- **Body:**
```json
{
  "refresh": "refresh_token_aqui"
}
```
- **Resposta:**
```json
{
  "access": "novo_access_token_aqui"
}
```

## Exemplo de Requisição e Resposta
### Criar um imóvel

**Endpoint:** `POST /imoveis/`

**Corpo da requisição:**
```json
{
  "titulo": "Casa com 3 quartos",
  "descricao": "Casa espaçosa no centro da cidade.",
  "endereco": "Rua Principal, 123",
  "bairro": "Centro",
  "preco_venda": 500000,
  "preco_locacao": 2000,
  "imobiliaria_id": 1,
  "destaque": true
}
```

**Resposta:**
```json
{
  "id": 1,
  "titulo": "Casa com 3 quartos",
  "descricao": "Casa espaçosa no centro da cidade.",
  "endereco": "Rua Principal, 123",
  "bairro": "Centro",
  "preco_venda": 500000,
  "preco_locacao": 2000,
  "imobiliaria_id": 1,
  "destaque": true,
  "data_criacao": "2023-10-01T12:00:00Z"
}
```

## Contato
- **Nome**: João
- **E-mail**: jvcbatist4@outlook.com
- **LinkedIn**: [LinkedIn](https://www.linkedin.com/in/soujoaovitor/)
