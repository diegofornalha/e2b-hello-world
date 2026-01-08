#!/usr/bin/env python3
"""
Chat CLI com Minimax/Claude rodando em E2B Sandbox

Arquitetura:
- Reutiliza módulos compartilhados de core/
- Loop interativo específico para terminal
"""

from core.config import MINIMAX_CONFIG, E2B_CONFIG, validate_config
from core.sandbox_manager import SandboxManager

# Validação automática ao importar config
validate_config()

def chat_loop(sandbox):
    """
    Loop interativo de chat no terminal

    Args:
        sandbox: Instância do sandbox E2B já configurado
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

            # Enviar mensagem usando SandboxManager do core
            print("\n🤖 Claude: ", end="", flush=True)
            response = SandboxManager.send_message(sandbox, user_input)

            # Exibir resposta
            print(response)

        except KeyboardInterrupt:
            print("\n\n👋 Chat interrompido. Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            break

def main():
    """Inicia chat CLI com sandbox E2B"""
    print("\n" + "=" * 60)
    print("🚀 Chat Minimax/Claude no E2B Sandbox")
    print("=" * 60)
    print(f"\n🤖 Modelo: {MINIMAX_CONFIG['model']}")
    print("🔒 Executando em sandbox isolado")
    print("=" * 60)

    try:
        print("\n📦 Criando sandbox E2B...")

        # Usar SandboxManager para criar e gerenciar sandbox
        with SandboxManager.create_sandbox() as sandbox:
            print(f"✅ Sandbox criado: {sandbox.sandbox_id}")

            # Configurar ambiente (instalar dependências)
            if not SandboxManager.setup_sandbox(sandbox):
                print("❌ Falha ao configurar chat")
                return

            # Iniciar loop de chat interativo
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
