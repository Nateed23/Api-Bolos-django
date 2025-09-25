

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
import re

from .models import User, Bolo, Pedido, ItemPedido, Categoria, ImagemBolo, ImagemPortfolio


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, 
        write_only=True, 
        required=True,
        label="Confirme a senha"
    )
    
    telefone = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r'^(21|24)\d{9}$',
                message="O número deve começar com o DDD 21 ou 24 e ter 11 dígitos no total."
            )
        ]
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'cep', 'logradouro', 'numero',
            'complemento', 'telefone', 'password', 'password2'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]}
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "As senhas não correspondem."})
        return data

    def validate_cep(self, value):
        if not re.match(r'^272\d{5}$', value):
            raise serializers.ValidationError("O CEP informado não pertence a Volta Redonda (deve iniciar com 272).")
        return value

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user



class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']

class ImagemBoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagemBolo
        fields = ['id', 'imagem']

class BoloSerializer(serializers.ModelSerializer):
    categorias = CategoriaSerializer(many=True, read_only=True)
    imagens = ImagemBoloSerializer(many=True, read_only=True)

    class Meta:
        model = Bolo
        fields = ['id', 'nome', 'preco', 'descricao', 'disponivel', 'imagem', 'categorias', 'imagens']

class ItemPedidoSerializer(serializers.ModelSerializer):
    bolo_nome = serializers.ReadOnlyField(source='bolo.nome')
    class Meta:
        model = ItemPedido
        fields = ['id', 'bolo', 'bolo_nome', 'quantidade', 'preco_unitario']

class PedidoSerializer(serializers.ModelSerializer):
    cliente = serializers.ReadOnlyField(source='cliente.username')
    itens = ItemPedidoSerializer(many=True, read_only=True)
    class Meta:
        model = Pedido
        fields = [
            'id', 'cliente', 'data_pedido', 'data_entrega', 'valor_total',
            'cep_entrega', 'logradouro_entrega', 'numero_entrega', 'complemento_entrega',
            'status', 'forma_pagamento', 'itens'
        ]

class ImagemPortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagemPortfolio
        fields = ['id', 'titulo', 'imagem', 'descricao']




class CriarItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ['bolo', 'quantidade']

class CriarPedidoSerializer(serializers.ModelSerializer):
    itens = CriarItemPedidoSerializer(many=True)
    class Meta:
        model = Pedido
        fields = [
            'data_entrega', 'cep_entrega', 'logradouro_entrega',
            'numero_entrega', 'complemento_entrega', 'forma_pagamento', 'itens'
        ]

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        valor_total_pedido = 0
        for item_data in itens_data:
            bolo = item_data['bolo']
            quantidade = item_data['quantidade']
            item = ItemPedido.objects.create(
                pedido=pedido,
                bolo=bolo,
                quantidade=quantidade,
                preco_unitario=bolo.preco
            )
            valor_total_pedido += item.get_subtotal()
        
        pedido.valor_total = valor_total_pedido
        pedido.save()
        
        return pedido
