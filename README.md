# API Marketplace de Imóveis

## Descrição
API para gerenciamento de imóveis, imobiliárias, pacotes de anúncios e contratos.

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

## Exemplo de Requisição e Resposta
### Criar um imóvel

**Endpoint:** `POST /imoveis/`

**Body:**
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

