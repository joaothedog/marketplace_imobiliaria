from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('IMOBILIARIA', 'Imobiliária'),
        ('NORMAL', 'Usuário Normal'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES)

    def __str__(self):
        return self.username

class ImobiliariaUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='imobiliaria')
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=255)

    def __str__(self):
        return self.nome

class NormalUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='normal_user')
    nome = models.CharField(max_length=255)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome
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

    class Meta:
        ordering = ['-data_criacao']

class Oferta(models.Model):
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, related_name='ofertas')
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ofertas')
    valor = models.DecimalField(max_digits=10, decimal_places=2)  # Valor da oferta
    tipo = models.CharField(max_length=10, choices=[('COMPRA', 'Compra'), ('LOCACAO', 'Locação')])  # Tipo de oferta
    data_criacao = models.DateTimeField(auto_now_add=True)  # Data da oferta

    def __str__(self):
        return f"Oferta de {self.tipo} por {self.usuario.username} no imóvel {self.imovel.titulo}"
    
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