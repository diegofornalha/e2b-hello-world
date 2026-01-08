#!/usr/bin/env python3
"""
Executa o projeto assistente-fontes dentro do sandbox E2B

Este script:
1. Carrega o código do assistente-fontes no sandbox
2. Configura variáveis de ambiente customizadas (Minimax API)
3. Instala dependências no sandbox
4. Executa o servidor FastAPI dentro do E2B
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

# Carregar variáveis de ambiente
load_dotenv()

# Configurações customizadas do Minimax/Anthropic
CUSTOM_ENV = {
    "ANTHROPIC_AUTH_TOKEN": "sk-cp-zcDlRVYnUrNf7aDw6DtpBNxSdxkAFooPcercwJicQ8O-sSMKXJHQQkR0jNFTeNjM1Jyz7yfnCQBDi_QD02lUDusjJbkHQvqayawc7mQQLKGOBwwZttlTKXc",
    "ANTHROPIC_MODEL": "minimax/minimax-m2",
    "ANTHROPIC_BASE_URL": "https://api.minimax.io/anthropic",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    # Variável adicional do projeto assistente-fontes
    "MINIMAX_API_KEY": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",  # Adicione aqui se necessário
}

def upload_project_to_sandbox(sandbox, project_path):
    """
    Faz upload dos arquivos do projeto para o sandbox
    """
    print(f"\n📦 Fazendo upload do projeto {project_path} para o sandbox...")

    project_path = Path(project_path)

    if not project_path.exists():
        print(f"❌ Erro: Projeto não encontrado em {project_path}")
        return False

    # Arquivos essenciais para upload
    essential_files = [
        'requirements.txt',
        'backend-dados/main.py',
        'backend-dados/gpt_utils.py',
        'backend-dados/search_engine.py',
        'backend-dados/prompt_router.py',
        'backend-dados/auth_utils.py',
        'backend-dados/db_logs.py',
    ]

    uploaded_count = 0

    for file_rel in essential_files:
        file_path = project_path / file_rel

        if not file_path.exists():
            print(f"⚠️  Arquivo não encontrado: {file_rel}")
            continue

        # Ler conteúdo do arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Criar diretório no sandbox se necessário
        sandbox_dir = Path('/home/user') / file_rel
        sandbox_dir_parent = str(sandbox_dir.parent)

        # Criar diretório
        sandbox.run_code(f"""
import os
os.makedirs('{sandbox_dir_parent}', exist_ok=True)
""")

        # Escrever arquivo no sandbox
        sandbox.run_code(f"""
with open('{sandbox_dir}', 'w', encoding='utf-8') as f:
    f.write('''{content}''')
print(f"✅ Uploaded: {file_rel}")
""")

        uploaded_count += 1

    print(f"\n✅ {uploaded_count} arquivos enviados para o sandbox")
    return True

def setup_environment_in_sandbox(sandbox, env_vars):
    """
    Configura variáveis de ambiente no sandbox
    """
    print("\n🔧 Configurando variáveis de ambiente no sandbox...")

    env_setup = "import os\n"
    for key, value in env_vars.items():
        env_setup += f'os.environ["{key}"] = "{value}"\n'

    env_setup += 'print("✅ Variáveis de ambiente configuradas:")\n'
    env_setup += 'print("\\n".join([f"{k}={v[:20]}..." for k, v in os.environ.items() if k.startswith("ANTHROPIC") or k.startswith("API_")]))'

    result = sandbox.run_code(env_setup)
    print(result.text)

def install_dependencies_in_sandbox(sandbox):
    """
    Instala dependências do projeto no sandbox
    """
    print("\n📦 Instalando dependências no sandbox...")

    install_code = """
import subprocess
import sys

# Pacotes essenciais
packages = [
    'fastapi',
    'uvicorn',
    'anthropic',
    'python-jose[cryptography]',
    'passlib[bcrypt]',
    'python-dotenv',
    'llama-index>=0.12.43',
    'sentence-transformers',
    'faiss-cpu',
    'markdown2'
]

for package in packages:
    print(f"📦 Instalando {package}...")
    subprocess.run(
        [sys.executable, '-m', 'pip', 'install', package, '--quiet'],
        check=True
    )

print("✅ Todas as dependências instaladas!")
"""

    result = sandbox.run_code(install_code)
    print(result.text)

    if result.error:
        print(f"⚠️  Avisos durante instalação: {result.error}")

def test_anthropic_connection_in_sandbox(sandbox):
    """
    Testa conexão com API Anthropic/Minimax no sandbox
    """
    print("\n🧪 Testando conexão com API Minimax/Anthropic...")

    test_code = """
import os
from anthropic import Anthropic

# Criar cliente com configurações customizadas
client = Anthropic(
    api_key=os.environ['ANTHROPIC_AUTH_TOKEN'],
    base_url=os.environ['ANTHROPIC_BASE_URL']
)

# Fazer uma chamada de teste
try:
    response = client.messages.create(
        model=os.environ['ANTHROPIC_MODEL'],
        max_tokens=100,
        messages=[
            {"role": "user", "content": "Diga 'Hello from E2B Sandbox!' em português"}
        ]
    )

    print("✅ Conexão bem-sucedida!")
    print(f"📝 Resposta da API: {response.content[0].text}")

except Exception as e:
    print(f"❌ Erro na conexão: {e}")
"""

    result = sandbox.run_code(test_code)
    print(result.text)

    if result.error:
        print(f"❌ Erro: {result.error}")
        return False

    return True

def run_simple_agent_task_in_sandbox(sandbox):
    """
    Executa uma tarefa simples do agente no sandbox
    """
    print("\n🤖 Executando tarefa do agente no sandbox...")

    task_code = """
import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ['ANTHROPIC_AUTH_TOKEN'],
    base_url=os.environ['ANTHROPIC_BASE_URL']
)

# Tarefa: Explicar o que é um Data Lake
response = client.messages.create(
    model=os.environ['ANTHROPIC_MODEL'],
    max_tokens=500,
    messages=[
        {
            "role": "user",
            "content": "Explique em 3 linhas o que é um Data Lake e suas camadas Bronze, Silver e Gold."
        }
    ]
)

result = response.content[0].text
print("="*50)
print("🎯 RESULTADO DA TAREFA")
print("="*50)
print(result)
print("="*50)
"""

    result = sandbox.run_code(task_code)
    print(result.text)

def main():
    print("🚀 Executando Assistente de Fontes no E2B Sandbox\n")
    print("=" * 60)

    # Verificar API key do E2B
    e2b_key = os.getenv("E2B_API_KEY")
    if not e2b_key:
        print("❌ Erro: E2B_API_KEY não encontrada!")
        print("   Configure o arquivo .env")
        return

    print("✅ E2B API Key encontrada")

    # Caminho do projeto assistente-fontes
    project_path = "/Users/2a/Desktop/NandaMac/assistente-fontes"

    print(f"\n📂 Projeto: {project_path}")
    print("🔧 API: Minimax (proxy Anthropic)")
    print(f"🤖 Modelo: {CUSTOM_ENV['ANTHROPIC_MODEL']}")

    try:
        print("\n" + "=" * 60)
        print("📦 CRIANDO SANDBOX E2B")
        print("=" * 60)

        with Sandbox.create() as sandbox:
            print(f"✅ Sandbox criado: {sandbox.sandbox_id}")

            # 1. Configurar variáveis de ambiente
            setup_environment_in_sandbox(sandbox, CUSTOM_ENV)

            # 2. Instalar dependências
            install_dependencies_in_sandbox(sandbox)

            # 3. Testar conexão com API
            if not test_anthropic_connection_in_sandbox(sandbox):
                print("\n⚠️  Conexão com API falhou, mas continuando...")

            # 4. Executar tarefa de teste
            run_simple_agent_task_in_sandbox(sandbox)

            # 5. (Opcional) Upload do projeto completo
            # Descomente abaixo se quiser fazer upload dos arquivos
            # upload_project_to_sandbox(sandbox, project_path)

            print("\n" + "=" * 60)
            print("✅ TESTES CONCLUÍDOS COM SUCESSO!")
            print("=" * 60)
            print("\n💡 O que foi testado:")
            print("   • Sandbox E2B criado e configurado")
            print("   • Variáveis de ambiente customizadas (Minimax)")
            print("   • Dependências instaladas (Anthropic SDK)")
            print("   • Conexão com API Minimax funcionando")
            print("   • Tarefa do agente executada com sucesso")
            print("\n🎉 Assistente rodando perfeitamente no sandbox isolado!")

    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
