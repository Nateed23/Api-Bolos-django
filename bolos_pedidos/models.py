from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date,timedelta


class User(AbstractUser):
    telefone = models.CharField("telefone",max_length=24)
    cep = models.CharField("cep",max_length=9)
    logradouro = models.CharField("Logradouro",max_length=120)
    numero = models.CharField("numero",max_length=20)
    complemento = models.CharField("complemento", max_length=150,blank=True,null=True)

    def __str__(self):
        return self.username


class Categoria(models.Model):
    nome = models.CharField(max_length=50,unique=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome

class Bolo(models.Model):
    nome = models.CharField(max_length=60)
    preco = models.DecimalField(max_digits=6,decimal_places=2)
    descricao = models.TextField()
    disponivel = models.BooleanField(default=True,help_text="marque se esta disponivel ")
    imagem = models.ImageField(upload_to='bolos/',null=True,blank=True, help_text="Imagem principal do bolo")
    categorias = models.ManyToManyField(Categoria, related_name='bolos') 

    class Meta:
        verbose_name = 'Bolo'
        verbose_name_plural = 'Bolos'

    def __str__(self):
        return f'{self.nome} - R${self.preco}'

class ImagemBolo(models.Model):
    bolo = models.ForeignKey(Bolo,on_delete=models.CASCADE, related_name='imagens')
    imagem= models.ImageField(upload_to='bolos/galeria/')

    def __str__(self):
        return f'Imagem para {self.bolo.nome}'


class Pedido(models.Model):
    STATUS_CHOICES = [
        ('em_preparo','em preparo'),
        ('entregue','Entregue'),
        ('cancelado','Cancelado'),
        ('aguardando_pagamento','Aguardando pagamento'),
    ]

    FORMA_PAGAMENTO = [
        ('pix','PIX'),
        ('dinheiro', 'DINHEIRO'),
        ('cartao','cartão credito/debito')
    ]

    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null= True, related_name='pedidos') 
    data_pedido = models.DateTimeField(auto_now_add=True)
    data_entrega = models.DateField(help_text='Data de Entrega da Encomenda')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    cep_entrega = models.CharField('Cep de entrega',max_length= 9 )
    logradouro_entrega = models.CharField('Logradouro de Entrega', max_length=150)
    numero_entrega = models.CharField('Numero da entrega' , max_length=20)
    complemento_entrega = models.CharField('Complemento da entrega', max_length=150, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='aguardando_pagamento')
    forma_pagamento = models.CharField(max_length=8,choices=FORMA_PAGAMENTO, default='pix')

    class Meta:
        ordering = ['-data_pedido']
        verbose_name = "pedido"
        verbose_name_plural = "Pedidos"


    def __str__(self):
        cliente_nome = self.cliente.username if self.cliente else "cliente removido"

        return f'pedido #{self.id} de {cliente_nome} - Status : {self.get_status_display()}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens') 
    bolo = models.ForeignKey(Bolo, on_delete=models.PROTECT, related_name='itens_pedidos')
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=8,decimal_places=2,help_text="preço do bolo no momento da compra")

    class Meta:
        verbose_name = "Item do pedido"
        verbose_name_plural = "Itens do pedido"
        unique_together = ('pedido','bolo')

    def __str__(self):
        return f'{self.quantidade}x{self.bolo.nome}'

    def get_subtotal(self):
        return self.quantidade * self.preco_unitario


class ImagemPortfolio(models.Model):
    titulo = models.CharField(max_length=100, help_text="Um título para a imagem, ex: 'Bolo de Casamento Floral'")
    imagem = models.ImageField(upload_to='portfolio/')
    descricao = models.TextField(blank=True, null=True, help_text="Descrição opcional da imagem.")

    class Meta:
        verbose_name = "Imagem do Portfólio"
        verbose_name_plural = "Imagens do Portfólio"
        ordering = ['-id'] 
    def __str__(self):
        return self.titulo