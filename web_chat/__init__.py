"""
web_chat - API de chat com Minimax/Claude em sandbox E2B

Este pacote fornece uma API HTTP para executar código Minimax/Claude
de forma isolada em sandboxes E2B.

Uso:
    # Como módulo Python
    python -m web_chat.server

    # Import programático
    from web_chat import app, SandboxManager

Estrutura:
    - config.py: Configurações centralizadas
    - models.py: Schemas Pydantic
    - utils.py: Funções auxiliares
    - minimax_client.py: Templates de código
    - sandbox_manager.py: Gerenciamento de sandboxes
    - routes.py: Endpoints HTTP
    - app.py: Aplicação FastAPI
    - server.py: Ponto de entrada
"""

from .app import app
from .server import main
from .sandbox_manager import SandboxManager

__version__ = "2.0.0"
__all__ = ["app", "main", "SandboxManager"]
