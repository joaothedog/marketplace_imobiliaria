from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Imobiliaria, Imovel, Imagem, PacoteAnuncio, Contrato, CustomUser, ImobiliariaUser, NormalUser, Oferta
from django.contrib.auth import authenticate

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'tipo_usuario']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            tipo_usuario=validated_data['tipo_usuario']
        )
        return user

class ImobiliariaUserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = ImobiliariaUser
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUserSerializer.create(CustomUserSerializer(), user_data)
        imobiliaria = ImobiliariaUser.objects.create(user=user, **validated_data)
        return imobiliaria

class NormalUserSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = NormalUser
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUserSerializer.create(CustomUserSerializer(), user_data)
        normal_user = NormalUser.objects.create(user=user, **validated_data)
        return normal_user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenciais inválidas.")

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

class OfertaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Oferta
        fields = '__all__'
        read_only_fields = ['usuario'] 

    def create(self, validated_data):  
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

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