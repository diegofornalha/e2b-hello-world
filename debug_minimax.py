#!/usr/bin/env python3
"""
Debug: Ver o que o Minimax retorna
"""
from e2b_code_interpreter import Sandbox
from dotenv import load_dotenv
import os

load_dotenv()

MINIMAX_TOKEN = "sk-cp-zcDlRVYnUrNf7aDw6DtpBNxSdxkAFooPcercwJicQ8O-sSMKXJHQQkR0jNFTeNjM1Jyz7yfnCQBDi_QD02lUDusjJbkHQvqayawc7mQQLKGOBwwZttlTKXc"

print("🔍 DEBUG: Testando resposta do Minimax\n")

with Sandbox.create() as sandbox:
    print("✅ Sandbox criado")

    # Instalar Anthropic
    sandbox.run_code("""
import subprocess, sys
subprocess.run([sys.executable, '-m', 'pip', 'install', 'anthropic', '--quiet'], check=True)
""")
    print("✅ Anthropic instalado\n")

    # Testar e fazer debug
    result = sandbox.run_code(f"""
from anthropic import Anthropic

client = Anthropic(
    api_key='{MINIMAX_TOKEN}',
    base_url='https://api.minimax.io/anthropic'
)

response = client.messages.create(
    model='minimax/minimax-m2',
    max_tokens=200,
    messages=[{{"role": "user", "content": "Diga apenas: Oi, estou funcionando!"}}]
)

print("="*60)
print("DEBUG: Tipo de response:", type(response))
print("DEBUG: Dir response:", [x for x in dir(response) if not x.startswith('_')])
print("="*60)

print("\\nDEBUG: response.content:", response.content)
print("DEBUG: Tamanho content:", len(response.content))

for i, block in enumerate(response.content):
    print(f"\\nDEBUG: Block {{i}}")
    print(f"  Tipo: {{type(block).__name__}}")
    print(f"  Atributos: {{[x for x in dir(block) if not x.startswith('_')]}}")

    if hasattr(block, 'text'):
        print(f"  Text attribute exists: '{{block.text}}'")
    if hasattr(block, 'thinking'):
        print(f"  Thinking attribute exists")
    if hasattr(block, '__dict__'):
        print(f"  Dict: {{block.__dict__}}")

print("="*60)

# Tentar extrair texto
answer = None
for block in response.content:
    if hasattr(block, 'text'):
        answer = block.text
        break

print(f"\\nFINAL ANSWER: '{{answer}}'")
""")

    print("\n📊 RESULTADO DO DEBUG:")
    print("="*60)
    print(result.text if result.text else "[VAZIO]")
    print("="*60)

    if result.error:
        print(f"\n❌ ERRO: {result.error}")
