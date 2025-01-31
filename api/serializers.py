from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import Imobiliaria, Imovel, Imagem, PacoteAnuncio, Contrato, UserProfile

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(write_only=True, required=False)
    is_imobiliaria = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'full_name', 'phone', 'is_imobiliaria']
        extra_kwargs = {
            'email': {'required': True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        # Cria o perfil do usuário
        UserProfile.objects.create(
            user=user,
            full_name=validated_data.get('full_name', ''),
            phone=validated_data.get('phone', ''),
            is_imobiliaria=validated_data.get('is_imobiliaria', False),
        )
        return user

class ImobiliariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imobiliaria
        fields = '__all__'

class ImovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imovel
        fields = '__all__'
        
    def validate_preco_venda(self, value):
        if value and value < 0:
            raise serializers.ValidationError("O preço de venda não pode ser negativo.")
        return value

    def validate_preco_locacao(self, value):
        if value and value < 0:
            raise serializers.ValidationError("O preço de locação não pode ser negativo.")
        return value

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