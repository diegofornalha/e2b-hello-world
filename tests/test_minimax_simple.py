#!/usr/bin/env python3
"""
Teste simples e direto do Minimax no E2B Sandbox
"""

import os
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()

# Configuração Minimax
MINIMAX_CONFIG = {
    "ANTHROPIC_AUTH_TOKEN": "sk-cp-zcDlRVYnUrNf7aDw6DtpBNxSdxkAFooPcercwJicQ8O-sSMKXJHQQkR0jNFTeNjM1Jyz7yfnCQBDi_QD02lUDusjJbkHQvqayawc7mQQLKGOBwwZttlTKXc",
    "ANTHROPIC_BASE_URL": "https://api.minimax.io/anthropic",
    "ANTHROPIC_MODEL": "minimax/minimax-m2",
}

def main():
    print("🚀 Teste Simples: Minimax no E2B\n")
    print("=" * 60)

    e2b_key = os.getenv("E2B_API_KEY")
    if not e2b_key:
        print("❌ E2B_API_KEY não encontrada!")
        return

    print("✅ E2B API Key OK")
    print("📦 Criando sandbox...\n")

    try:
        with Sandbox.create() as sandbox:
            print(f"✅ Sandbox criado: {sandbox.sandbox_id}\n")

            # Instalar Anthropic SDK
            print("📦 Instalando Anthropic SDK...")
            result = sandbox.run_code("""
import subprocess
import sys
subprocess.run([sys.executable, '-m', 'pip', 'install', 'anthropic', '--quiet'], check=True)
print("✅ Anthropic SDK instalado!")
""")
            print(result.text)

            # Configurar e testar
            print("\n🧪 Testando Minimax API...\n")
            result = sandbox.run_code(f"""
import os
from anthropic import Anthropic

# Configurar
os.environ['ANTHROPIC_AUTH_TOKEN'] = '{MINIMAX_CONFIG["ANTHROPIC_AUTH_TOKEN"]}'
os.environ['ANTHROPIC_BASE_URL'] = '{MINIMAX_CONFIG["ANTHROPIC_BASE_URL"]}'

# Criar cliente
client = Anthropic(
    api_key=os.environ['ANTHROPIC_AUTH_TOKEN'],
    base_url=os.environ['ANTHROPIC_BASE_URL']
)

# Testar com pergunta simples
response = client.messages.create(
    model='{MINIMAX_CONFIG["ANTHROPIC_MODEL"]}',
    max_tokens=300,
    messages=[
        {{"role": "user", "content": "Explique em 2 linhas o que é um sandbox de computação."}}
    ]
)

print("✅ Conexão bem-sucedida!")
print("\\n📝 Resposta do Minimax/Claude:")
print("-" * 60)
print(response.content[0].text)
print("-" * 60)
""")

            print(result.text)

            if result.error:
                print(f"\n⚠️  Erro: {result.error}")
            else:
                print("\n" + "=" * 60)
                print("✅ TESTE PASSOU COM SUCESSO!")
                print("=" * 60)
                print("\n💡 Comprovado:")
                print("   • Sandbox E2B isolado criado")
                print("   • Anthropic SDK instalado no sandbox")
                print("   • Minimax API configurada e funcionando")
                print("   • Resposta do Claude recebida")
                print("   • Seu computador permanece intocado")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
