# API Marketplace de Imóveis

## Descrição
API para gerenciamento de imóveis, imobiliárias, pacotes de anúncios e contratos.

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

A API estará disponível em `http://127.0.0.1:8000/api/`.

## Endpoints

### Imobiliárias
- **GET /imobiliarias/** - Listar todas as imobiliárias.
- **POST /imobiliarias/** - Criar uma nova imobiliária.
- **GET /imobiliarias/{id}/** - Detalhes de uma imobiliária.
- **PUT /imobiliarias/{id}/** - Atualizar uma imobiliária.
- **DELETE /imobiliarias/{id}/** - Excluir uma imobiliária.

### Imóveis
- **GET /imoveis/** - Listar todos os imóveis (com filtros: bairro, preço, tipo).
- **POST /imoveis/** - Criar um novo imóvel.
- **GET /imoveis/{id}/** - Detalhes de um imóvel.
- **PUT /imoveis/{id}/** - Atualizar um imóvel.
- **DELETE /imoveis/{id}/** - Excluir um imóvel.

### Imagens
- **POST /imoveis/{id}/imagens/** - Adicionar imagem a um imóvel.
- **DELETE /imagens/{id}/** - Excluir uma imagem.

### Pacotes de Anúncios
- **GET /pacotes/** - Listar todos os pacotes.
- **POST /pacotes/** - Criar um novo pacote.
- **GET /pacotes/{id}/** - Detalhes de um pacote.
- **PUT /pacotes/{id}/** - Atualizar um pacote.
- **DELETE /pacotes/{id}/** - Excluir um pacote.

### Contratos
- **GET /contratos/** - Listar todos os contratos.
- **POST /contratos/** - Criar um novo contrato.
- **GET /contratos/{id}/** - Detalhes de um contrato.
- **PUT /contratos/{id}/** - Atualizar um contrato.
- **DELETE /contratos/{id}/** - Excluir um contrato.

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