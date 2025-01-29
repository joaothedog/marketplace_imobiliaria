from rest_framework import serializers
from .models import Imobiliaria, Imovel, Imagem, PacoteAnuncio, Contrato

class ImobiliariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imobiliaria
        fields = '__all__'

class ImovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imovel
        fields = '__all__'

class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = '__all__'

class PacoteAnuncioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacoteAnuncio
        fields = '__all__'

class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contrato
        fields = '__all__'