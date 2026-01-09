from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from claude_mini_sdk.config import SERVER_CONFIG
from .routes import router

def create_app() -> FastAPI:
    """
    Factory function para criar aplicação FastAPI

    Configura:
    - Metadata da API (título, descrição, versão)
    - Middleware CORS com origens restritas
    - Rotas HTTP

    Returns:
        FastAPI: Instância configurada da aplicação
    """
    app = FastAPI(
        title="Claude E2B API",
        description="API que executa Minimax/Claude em sandbox E2B isolado",
        version="2.0.0"
    )

    # CORS configurável (não mais wildcard *)
    # Apenas localhost permitido por padrão
    app.add_middleware(
        CORSMiddleware,
        allow_origins=SERVER_CONFIG["cors_origins"],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
        allow_credentials=True
    )

    # Registrar rotas
    app.include_router(router)

    return app

# Instância global para uvicorn
app = create_app()
