from .config import MINIMAX_CONFIG
from .utils import escape_for_python_code

def get_install_dependencies_code() -> str:
    return

def get_chat_code(user_message: str) -> str:
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
    system="Responda sempre em português brasileiro (pt-BR). Use linguagem natural e clara. Código e termos técnicos podem permanecer em inglês quando apropriado.",
    messages=[{{"role": "user", "content": "{msg_safe}"}}]
)

"""
