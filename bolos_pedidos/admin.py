# bolo_pedidos/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Adicione ImagemPortfolio à importação
from .models import User, Bolo, Pedido, ItemPedido, Categoria, ImagemBolo, ImagemPortfolio

# --- Classes Inline ---
class ImagemBoloInline(admin.TabularInline):
    model = ImagemBolo
    extra = 1

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    readonly_fields = ('preco_unitario',)

# --- Classes Admin ---
class BoloAdmin(admin.ModelAdmin):
    inlines = [ImagemBoloInline]
    list_display = ('nome', 'preco', 'disponivel')
    search_fields = ('nome', 'descricao')
    list_filter = ('disponivel', 'categorias')

class PedidoAdmin(admin.ModelAdmin):
    inlines = [ItemPedidoInline]
    list_display = ('id', 'cliente', 'data_pedido', 'status', 'valor_total')
    search_fields = ('cliente__username', 'id')
    list_filter = ('status', 'forma_pagamento', 'data_entrega')
    readonly_fields = ('valor_total', 'data_pedido')

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        *BaseUserAdmin.fieldsets,
        (
            'Informações Adicionais',
            {
                'fields': ('telefone', 'cep', 'logradouro', 'numero', 'complemento'),
            },
        ),
    )

# --- Registo dos modelos ---
admin.site.register(User, UserAdmin)
admin.site.register(Bolo, BoloAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Categoria)
# --- ADICIONE ESTA LINHA ---
admin.site.register(ImagemPortfolio)
