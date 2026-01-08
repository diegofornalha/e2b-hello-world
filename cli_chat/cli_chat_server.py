#!/usr/bin/env python3
"""
Chat com Minimax/Claude rodando dentro do E2B Sandbox

Arquitetura:
┌─────────────────────────┐
│ Seu Computador (Local)  │
│ • Este script Python    │
└───────────┬─────────────┘
            │ API E2B
            ▼
┌─────────────────────────┐
│ E2B Cloud Sandbox       │
│ ┌─────────────────────┐ │
│ │ Anthropic Client    │ │
│ │ + Minimax API       │ │
│ └─────────────────────┘ │
└─────────────────────────┘
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

# Carregar .env da raiz do projeto
load_dotenv(Path(__file__).parent.parent / ".env")

# Credenciais Minimax (do .env)
MINIMAX_TOKEN = os.getenv("MINIMAX_TOKEN")

MINIMAX_CONFIG = {
    "ANTHROPIC_AUTH_TOKEN": MINIMAX_TOKEN,
    "ANTHROPIC_MODEL": "minimax/minimax-m2",
    "ANTHROPIC_BASE_URL": "https://api.minimax.io/anthropic",
}

def setup_chat_in_sandbox(sandbox):
    """
    Configura o ambiente de chat no sandbox E2B
    """
    print("🔧 Configurando chat no sandbox...")

    setup_code = f"""
import subprocess
import sys
import os

# Instalar Anthropic SDK
print("📦 Instalando Anthropic SDK...")
subprocess.run([sys.executable, '-m', 'pip', 'install', 'anthropic', '--quiet'], check=True)

# Configurar credenciais
os.environ['ANTHROPIC_AUTH_TOKEN'] = '{MINIMAX_CONFIG["ANTHROPIC_AUTH_TOKEN"]}'
os.environ['ANTHROPIC_BASE_URL'] = '{MINIMAX_CONFIG["ANTHROPIC_BASE_URL"]}'
os.environ['ANTHROPIC_MODEL'] = '{MINIMAX_CONFIG["ANTHROPIC_MODEL"]}'

print("✅ Chat configurado e pronto!")
"""

    result = sandbox.run_code(setup_code)
    print(result.text)

    if result.error:
        print(f"⚠️  Avisos: {result.error}")
        return False

    return True

def send_message_in_sandbox(sandbox, user_message):
    """
    Envia mensagem para o Claude/Minimax dentro do sandbox
    """
    # Escapar aspas na mensagem
    safe_message = user_message.replace('"', '\\"').replace("'", "\\'")

    chat_code = f"""
import os
from anthropic import Anthropic

# Criar cliente com configuração Minimax
client = Anthropic(
    api_key=os.environ['ANTHROPIC_AUTH_TOKEN'],
    base_url=os.environ['ANTHROPIC_BASE_URL']
)

# Enviar mensagem
try:
    response = client.messages.create(
        model=os.environ['ANTHROPIC_MODEL'],
        max_tokens=2000,
        messages=[
            {{"role": "user", "content": "{safe_message}"}}
        ]
    )

    # Extrair resposta
    answer = response.content[0].text
    print(answer)

except Exception as e:
    print(f"❌ Erro: {{e}}")
"""

    result = sandbox.run_code(chat_code)
    return result.text

def chat_loop(sandbox):
    """
    Loop interativo de chat
    """
    print("\n" + "=" * 60)
    print("💬 CHAT COM CLAUDE/MINIMAX (rodando no E2B Sandbox)")
    print("=" * 60)
    print("\n🤖 Claude: Olá! Como posso ajudar você hoje?")
    print("\n💡 Digite 'sair' para encerrar o chat")
    print("=" * 60)

    while True:
        try:
            # Obter mensagem do usuário
            user_input = input("\n👤 Você: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['sair', 'exit', 'quit']:
                print("\n👋 Encerrando chat. Até logo!")
                break

            # Enviar para o sandbox
            print("\n🤖 Claude: ", end="", flush=True)
            response = send_message_in_sandbox(sandbox, user_input)

            # Exibir resposta
            print(response)

        except KeyboardInterrupt:
            print("\n\n👋 Chat interrompido. Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            break

def main():
    print("🚀 Chat Minimax/Claude no E2B Sandbox\n")
    print("=" * 60)

    # Verificar E2B API key
    e2b_key = os.getenv("E2B_API_KEY")
    if not e2b_key:
        print("❌ Erro: E2B_API_KEY não encontrada!")
        print("   Configure o arquivo .env")
        return

    print("✅ E2B API Key encontrada")
    print("🔧 API: Minimax (proxy Anthropic)")
    print(f"🤖 Modelo: {MINIMAX_CONFIG['ANTHROPIC_MODEL']}")

    try:
        print("\n📦 Criando sandbox E2B...")

        with Sandbox.create() as sandbox:
            print(f"✅ Sandbox criado: {sandbox.sandbox_id}")

            # Configurar ambiente
            if not setup_chat_in_sandbox(sandbox):
                print("❌ Falha ao configurar chat")
                return

            # Iniciar loop de chat
            chat_loop(sandbox)

            print("\n" + "=" * 60)
            print("✅ Chat encerrado!")
            print("🗑️  Sandbox será destruído automaticamente")
            print("=" * 60)

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
