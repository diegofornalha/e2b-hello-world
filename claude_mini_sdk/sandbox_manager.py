from e2b_code_interpreter import Sandbox
from .config import E2B_CONFIG, MINIMAX_CONFIG
from .minimax_client import get_install_dependencies_code, get_chat_code
from .utils import truncate_log

class SandboxManager:
    @staticmethod
    def create_sandbox() -> Sandbox:
        return Sandbox.create(timeout=E2B_CONFIG["timeout"])

    @staticmethod
    def setup_sandbox(sandbox: Sandbox) -> bool:
        try:
            print("📦 Instalando dependências no sandbox...")
            sandbox.run_code(get_install_dependencies_code())
            print("✅ Sandbox configurado")
            return True

        except Exception as e:
            print(f"❌ Erro ao configurar sandbox: {e}")
            return False

    @staticmethod
    def send_message(sandbox: Sandbox, message: str) -> str:
        try:
            print(f"📨 Mensagem: {truncate_log(message, 50)}")

            # Gerar código com token vindo de env var (seguro)
            code = get_chat_code(message)

            # Executar no sandbox
            print("🤖 Chamando Minimax API...")
            result = sandbox.run_code(code)

            # Capturar resposta
            response = result.text or ""

            if result.error:
                print(f"⚠️  Aviso do sandbox: {result.error}")

            print(f"✅ Resposta: {truncate_log(response)}")

            return response

        except Exception as e:
            error_msg = f"Erro ao processar mensagem: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
