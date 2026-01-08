#!/usr/bin/env python3
"""
Debug 2: Ver se há erros
"""
from e2b_code_interpreter import Sandbox
from dotenv import load_dotenv

load_dotenv()

MINIMAX_TOKEN = "sk-cp-zcDlRVYnUrNf7aDw6DtpBNxSdxkAFooPcercwJicQ8O-sSMKXJHQQkR0jNFTeNjM1Jyz7yfnCQBDi_QD02lUDusjJbkHQvqayawc7mQQLKGOBwwZttlTKXc"

print("🔍 DEBUG 2: Checando erros\n")

with Sandbox.create() as sandbox:
    print("✅ Sandbox criado")

    # Instalar
    sandbox.run_code("""
import subprocess, sys
subprocess.run([sys.executable, '-m', 'pip', 'install', 'anthropic', '--quiet'], check=True)
""")
    print("✅ Anthropic instalado\n")

    # Teste simples primeiro
    print("📝 Teste 1: Print simples")
    result1 = sandbox.run_code("print('Hello World')")
    print(f"   Text: '{result1.text}'")
    print(f"   Error: {result1.error}")

    print("\n📝 Teste 2: Chamar Minimax")
    result2 = sandbox.run_code(f"""
try:
    from anthropic import Anthropic

    client = Anthropic(
        api_key='{MINIMAX_TOKEN}',
        base_url='https://api.minimax.io/anthropic'
    )

    response = client.messages.create(
        model='minimax/minimax-m2',
        max_tokens=100,
        messages=[{{"role": "user", "content": "Diga: Oi!"}}]
    )

    print("Chamada bem-sucedida!")
    print(f"Content blocks: {{len(response.content)}}")

    for block in response.content:
        print(f"Block type: {{type(block).__name__}}")

except Exception as e:
    print(f"ERRO: {{e}}")
    import traceback
    traceback.print_exc()
""")

    print(f"\n📊 Resultado:")
    print(f"   Text: '{result2.text}'")
    print(f"   Error: {result2.error}")
