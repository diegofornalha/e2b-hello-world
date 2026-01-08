#!/usr/bin/env python3
"""
Explorar o filesystem do sandbox E2B
"""
from e2b_code_interpreter import Sandbox
from dotenv import load_dotenv

load_dotenv()

print("🔍 Explorando filesystem do sandbox E2B\n")
print("="*60)

with Sandbox.create() as sandbox:
    print(f"✅ Sandbox criado: {sandbox.sandbox_id}\n")

    # Verificar estrutura de diretórios
    print("📁 Estrutura do diretório home:")
    result = sandbox.run_code("""
import os
import subprocess

# Diretório atual
print(f"📍 Diretório atual: {os.getcwd()}")
print(f"📍 Home: {os.path.expanduser('~')}")
print(f"📍 User: {os.getenv('USER', 'unknown')}")

print("\\n" + "="*60)
print("📂 Listando /home/user:")
print("="*60)
result = subprocess.run(['ls', '-la', '/home/user'], capture_output=True, text=True)
print(result.stdout)

print("\\n" + "="*60)
print("🔍 Procurando pasta .claude:")
print("="*60)

# Verificar se .claude existe
claude_path = os.path.expanduser('~/.claude')
if os.path.exists(claude_path):
    print(f"✅ Pasta .claude ENCONTRADA em: {claude_path}")

    # Listar conteúdo
    print(f"\\n📂 Conteúdo de {claude_path}:")
    result = subprocess.run(['ls', '-la', claude_path], capture_output=True, text=True)
    print(result.stdout)

    # Procurar arquivos específicos
    result = subprocess.run(['find', claude_path, '-type', 'f'], capture_output=True, text=True)
    if result.stdout:
        print(f"\\n📄 Arquivos encontrados:")
        print(result.stdout)
else:
    print(f"❌ Pasta .claude NÃO existe em: {claude_path}")

print("\\n" + "="*60)
print("🔍 Procurando em todo /home:")
print("="*60)
result = subprocess.run(['find', '/home', '-name', '.claude', '-type', 'd'], capture_output=True, text=True)
if result.stdout:
    print(f"✅ Encontrado em:")
    print(result.stdout)
else:
    print("❌ Pasta .claude não encontrada em /home")

print("\\n" + "="*60)
print("🔍 Verificando variáveis de ambiente Claude:")
print("="*60)
claude_vars = {k: v for k, v in os.environ.items() if 'CLAUDE' in k.upper() or 'ANTHROPIC' in k.upper()}
if claude_vars:
    for k, v in claude_vars.items():
        print(f"   {k}={v[:50]}..." if len(v) > 50 else f"   {k}={v}")
else:
    print("❌ Nenhuma variável Claude/Anthropic configurada")
""")

    print("\n📊 RESULTADO DA EXPLORAÇÃO:")
    print("="*60)
    if result.logs and result.logs.stdout:
        print("".join(result.logs.stdout))
    else:
        print(result.text or "[Sem output]")
    print("="*60)

    if result.error:
        print(f"\n❌ Erro: {result.error}")
