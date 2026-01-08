#!/usr/bin/env python3
"""
E2B Hello World - Teste básico de sandbox

Este script demonstra como:
1. Criar um sandbox E2B
2. Executar código Python dentro dele
3. Capturar e exibir resultados
"""

import os
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

# Carregar variáveis de ambiente
load_dotenv()

def main():
    print("🚀 E2B Hello World\n")
    print("=" * 50)

    # Verificar se a API key está configurada
    api_key = os.getenv("E2B_API_KEY")
    if not api_key:
        print("❌ Erro: E2B_API_KEY não encontrada!")
        print("   Configure o arquivo .env com sua API key")
        print("   Obtenha em: https://e2b.dev/dashboard?tab=keys")
        return

    print("✅ API Key encontrada")
    print("\n📦 Criando sandbox E2B...")

    try:
        # Criar sandbox
        with Sandbox.create() as sandbox:
            print("✅ Sandbox criado com sucesso!")
            print(f"   Sandbox ID: {sandbox.sandbox_id}")

            print("\n🔧 Executando código no sandbox...")

            # Teste 1: Operação matemática simples
            print("\n[Teste 1] Operação matemática:")
            result = sandbox.run_code("2 + 2")
            print(f"   Código: 2 + 2")
            print(f"   Resultado: {result.text}")

            # Teste 2: Criando variável e usando
            print("\n[Teste 2] Manipulação de variáveis:")
            sandbox.run_code("x = 10")
            result = sandbox.run_code("x * 5")
            print(f"   Código: x = 10; x * 5")
            print(f"   Resultado: {result.text}")

            # Teste 3: Executar comando bash
            print("\n[Teste 3] Executando comando bash:")
            result = sandbox.run_code("import subprocess; subprocess.run(['echo', 'Hello from E2B!'], capture_output=True).stdout.decode()")
            print(f"   Comando: echo 'Hello from E2B!'")
            print(f"   Resultado: {result.text}")

            # Teste 4: Ver informações do sistema
            print("\n[Teste 4] Informações do sistema:")
            result = sandbox.run_code("""
import platform
import sys

info = {
    'Python': sys.version.split()[0],
    'OS': platform.system(),
    'Arquitetura': platform.machine()
}
info
""")
            print(f"   Resultado: {result.text}")

            print("\n" + "=" * 50)
            print("✅ Todos os testes passaram!")
            print("🎉 Sandbox E2B funcionando perfeitamente!")

    except Exception as e:
        print(f"\n❌ Erro ao criar/usar sandbox: {e}")
        print("   Verifique se sua API key está válida")
        return

if __name__ == "__main__":
    main()
