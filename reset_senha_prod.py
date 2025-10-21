# reset_senha_prod.py

import os
import django

# 1. CONFIGURAÇÃO DO DJANGO: Substitua 'seu_projeto' pelo nome da sua pasta de projeto
# Exemplo: Se seu settings.py está em 'backend_jucks/settings.py', use 'backend_jucks'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_jucks.settings') 
django.setup()

from django.contrib.auth import get_user_model

# --- DADOS DE ALVO ---
USERNAME_TO_CHANGE = 'madamejussara'
# COLOQUE A NOVA SENHA AQUI, DE FORMA SEGURA E FORTE
NEW_PASSWORD = 'N@at10102010' 
# ---------------------

User = get_user_model()

try:
    user = User.objects.get(username=USERNAME_TO_CHANGE)
    
    # Define e salva a nova senha
    user.set_password(NEW_PASSWORD)
    user.save()
    
    print(f"SUCESSO: Senha alterada para o usuário '{USERNAME_TO_CHANGE}'.")

except User.DoesNotExist:
    print(f"ERRO: Usuário '{USERNAME_TO_CHANGE}' não encontrado no banco de dados de produção.")
except Exception as e:
    print(f"ERRO inesperado ao alterar senha: {e}")