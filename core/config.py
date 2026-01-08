import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env da raiz do projeto
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

# Configurações Minimax/Claude
MINIMAX_CONFIG = {
    "token": os.getenv("MINIMAX_TOKEN"),
    "model": "minimax/minimax-m2",
    "base_url": "https://api.minimax.io/anthropic",
    "max_tokens": 800
}

# Configurações E2B
E2B_CONFIG = {
    "api_key": os.getenv("E2B_API_KEY"),
    "timeout": 180  # segundos
}

# Configurações do servidor HTTP
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "cors_origins": ["http://localhost:8000"]  # Restringir CORS para segurança
}

def validate_config():
    """Valida se todas as credenciais obrigatórias estão configuradas"""
    if not MINIMAX_CONFIG["token"]:
        raise ValueError(
            "MINIMAX_TOKEN não configurado no .env\n"
            "Configure o arquivo .env com sua API key"
        )
    if not E2B_CONFIG["api_key"]:
        raise ValueError(
            "E2B_API_KEY não configurado no .env\n"
            "Obtenha em: https://e2b.dev/dashboard?tab=keys"
        )

# Validar configurações no import
validate_config()
