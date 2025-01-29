from django.db import models

class Imobiliaria(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class Imovel(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    preco_locacao = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    imobiliaria = models.ForeignKey(Imobiliaria, on_delete=models.CASCADE, related_name='imoveis')
    destaque = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
class Imagem(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name='imagens')
    url = models.URLField()

    def __str__(self):
        return f"Imagem {self.id} - {self.imovel.titulo}"
    
class PacoteAnuncio(models.Model):
    nome = models.CharField(max_length=100)
    quantidade_anuncios = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

class Contrato(models.Model):
    imobiliaria = models.ForeignKey(Imobiliaria, on_delete=models.CASCADE, related_name='contratos')
    pacote = models.ForeignKey(PacoteAnuncio, on_delete=models.CASCADE)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Contrato {self.id} - {self.imobiliaria.nome}"