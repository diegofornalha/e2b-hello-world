#!/usr/bin/env python3
"""
Claude Agent SDK rodando dentro do E2B Sandbox

Este script demonstra como executar o Claude Agent SDK
de forma segura dentro de um sandbox E2B isolado.

Arquitetura:
1. Script local cria sandbox E2B
2. Instala Claude Agent SDK no sandbox
3. Executa tarefas do agente isoladamente
4. Retorna resultados para o script local
"""

import os
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

# Carregar variáveis de ambiente
load_dotenv()

def setup_agent_in_sandbox(sandbox, anthropic_key):
    """
    Instala e configura o Claude Agent SDK dentro do sandbox E2B
    """
    print("📦 Instalando Claude Agent SDK no sandbox...")

    # Instalar pacotes necessários
    setup_code = f"""
import subprocess
import sys

# Instalar anthropic SDK
subprocess.run([sys.executable, '-m', 'pip', 'install', 'anthropic', '--quiet'], check=True)

# Configurar API key
import os
os.environ['ANTHROPIC_API_KEY'] = '{anthropic_key}'

print("✅ Claude Agent SDK instalado e configurado!")
"""

    result = sandbox.run_code(setup_code)
    print(result.text)
    return result.error is None

def run_agent_task(sandbox, task):
    """
    Executa uma tarefa usando o Claude no sandbox
    """
    print(f"\n🤖 Executando tarefa: {task}")

    agent_code = f"""
from anthropic import Anthropic

client = Anthropic()

# Executar tarefa
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {{"role": "user", "content": "{task}"}}
    ]
)

# Retornar resultado
response.content[0].text
"""

    result = sandbox.run_code(agent_code)

    if result.error:
        print(f"❌ Erro: {result.error}")
        return None

    return result.text

def main():
    print("🚀 Claude Agent SDK + E2B Sandbox\n")
    print("=" * 50)

    # Verificar API keys
    e2b_key = os.getenv("E2B_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")

    if not e2b_key:
        print("❌ Erro: E2B_API_KEY não encontrada!")
        print("   Obtenha em: https://e2b.dev/dashboard?tab=keys")
        return

    if not anthropic_key:
        print("❌ Erro: ANTHROPIC_API_KEY não encontrada!")
        print("   Obtenha em: https://console.anthropic.com/")
        return

    print("✅ API Keys encontradas")
    print("\n📦 Criando sandbox E2B...")

    try:
        with Sandbox.create() as sandbox:
            print(f"✅ Sandbox criado: {sandbox.sandbox_id}")

            # Setup do agente no sandbox
            if not setup_agent_in_sandbox(sandbox, anthropic_key):
                print("❌ Falha ao configurar agente")
                return

            print("\n" + "=" * 50)
            print("🎯 TESTES DO AGENTE NO SANDBOX")
            print("=" * 50)

            # Teste 1: Pergunta simples
            result = run_agent_task(
                sandbox,
                "Explique em uma frase o que é um sandbox em computação."
            )
            if result:
                print(f"\n📝 Resposta do agente:\n{result}")

            # Teste 2: Gerar código
            result = run_agent_task(
                sandbox,
                "Escreva uma função Python que retorna os 10 primeiros números da sequência Fibonacci."
            )
            if result:
                print(f"\n📝 Resposta do agente:\n{result}")

            print("\n" + "=" * 50)
            print("✅ Testes concluídos!")
            print("🎉 Claude Agent SDK rodando com sucesso no E2B!")
            print("\n💡 Benefícios dessa arquitetura:")
            print("   • Código do agente isolado do seu sistema")
            print("   • Segredos de produção protegidos")
            print("   • Execução segura e escalável")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
