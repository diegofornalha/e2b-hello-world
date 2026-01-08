"""
Templates de código Python para executar no sandbox E2B

Este módulo gera código Python que será executado dentro do sandbox
para instalar dependências e chamar a API Minimax/Claude.
"""

from .config import MINIMAX_CONFIG
from .utils import escape_for_python_code

def get_install_dependencies_code() -> str:
    """
    Retorna código Python para instalar Anthropic SDK no sandbox

    Returns:
        String com código Python para executar via sandbox.run_code()
    """
    return """
import subprocess, sys
subprocess.run([sys.executable, '-m', 'pip', 'install', 'anthropic', '--quiet'])
"""

def get_chat_code(user_message: str) -> str:
    """
    Gera código Python para chamar Minimax API com mensagem do usuário

    Args:
        user_message: Mensagem do usuário (será escapada automaticamente)

    Returns:
        String com código Python completo para executar no sandbox
    """
    msg_safe = escape_for_python_code(user_message)

    return f"""
from anthropic import Anthropic

client = Anthropic(
    api_key='{MINIMAX_CONFIG["token"]}',
    base_url='{MINIMAX_CONFIG["base_url"]}'
)

resp = client.messages.create(
    model='{MINIMAX_CONFIG["model"]}',
    max_tokens={MINIMAX_CONFIG["max_tokens"]},
    messages=[{{"role": "user", "content": "{msg_safe}"}}]
)

# Extrair texto da resposta
texto = ""
for bloco in resp.content:
    if hasattr(bloco, 'text'):
        texto = bloco.text
        break

# Retornar como última expressão (sandbox.run_code captura isso)
texto if texto else "Olá! Sistema funcionando."
"""
