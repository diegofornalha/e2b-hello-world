#!/usr/bin/env python3
"""
Teste Minimax no E2B - Versão corrigida para lidar com ThinkingBlock
"""

import os
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()

MINIMAX_CONFIG = {
    "ANTHROPIC_AUTH_TOKEN": "sk-cp-zcDlRVYnUrNf7aDw6DtpBNxSdxkAFooPcercwJicQ8O-sSMKXJHQQkR0jNFTeNjM1Jyz7yfnCQBDi_QD02lUDusjJbkHQvqayawc7mQQLKGOBwwZttlTKXc",
    "ANTHROPIC_BASE_URL": "https://api.minimax.io/anthropic",
    "ANTHROPIC_MODEL": "minimax/minimax-m2",
}

def main():
    print("🚀 Teste Minimax no E2B (Versão Corrigida)\n")
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

            # Configurar e testar com tratamento de diferentes tipos de blocos
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

try:
    # Fazer request
    response = client.messages.create(
        model='{MINIMAX_CONFIG["ANTHROPIC_MODEL"]}',
        max_tokens=500,
        messages=[
            {{"role": "user", "content": "Explique em uma frase curta: o que é um sandbox?"}}
        ]
    )

    print("✅ Conexão bem-sucedida!")
    print("\\n📊 Tipo de resposta recebida:")
    print(f"   Model: {{response.model}}")
    print(f"   Role: {{response.role}}")
    print(f"   Blocos de conteúdo: {{len(response.content)}}")

    print("\\n📝 Conteúdo da resposta:")
    print("-" * 60)

    # Processar todos os blocos de conteúdo
    for i, block in enumerate(response.content):
        print(f"\\n[Bloco {{i+1}}] Tipo: {{type(block).__name__}}")

        # Verificar tipo de bloco
        if hasattr(block, 'text'):
            print(f"Texto: {{block.text}}")
        elif hasattr(block, 'thinking'):
            print(f"Pensamento (interno): {{block.thinking}}")
        elif hasattr(block, 'type'):
            print(f"Tipo especial: {{block.type}}")
            if hasattr(block, '__dict__'):
                print(f"Atributos: {{block.__dict__}}")
        else:
            print(f"Bloco desconhecido: {{block}}")

    print("-" * 60)

except Exception as e:
    print(f"❌ Erro na chamada: {{e}}")
    import traceback
    traceback.print_exc()
""")

            print(result.text)

            if result.error:
                print(f"\n⚠️  Detalhes do erro:\n{result.error}")
            else:
                print("\n" + "=" * 60)
                print("✅ TESTE COMPLETO!")
                print("=" * 60)

    except Exception as e:
        print(f"\n❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
