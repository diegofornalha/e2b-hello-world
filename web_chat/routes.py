from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

from .models import ChatRequest, ChatResponse, HealthResponse
from claude_mini_sdk.sandbox_manager import SandboxManager
from claude_mini_sdk.config import MINIMAX_CONFIG

router = APIRouter()
CURRENT_DIR = Path(__file__).parent

@router.get("/")
async def home():
    """
    Serve arquivo HTML do frontend

    Returns:
        FileResponse: index.html com interface de chat

    Raises:
        HTTPException: 404 se index.html não existir
    """
    html_path = CURRENT_DIR / "static" / "index.html"
    if not html_path.exists():
        raise HTTPException(
            status_code=404,
            detail="index.html não encontrado"
        )
    return FileResponse(html_path)

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Processa mensagem do usuário usando sandbox E2B + Minimax API

    Fluxo:
    1. Cria novo sandbox E2B (isolamento total)
    2. Instala dependências (Anthropic SDK)
    3. Configura variáveis de ambiente
    4. Executa código Python que chama Minimax API
    5. Retorna resposta do modelo

    Args:
        req: ChatRequest com mensagem do usuário

    Returns:
        ChatResponse: Resposta do modelo + sandbox_id

    Raises:
        HTTPException: 500 se falhar ao criar sandbox ou processar mensagem
    """
    try:
        # Criar sandbox novo a cada request (mais confiável)
        with SandboxManager.create_sandbox() as sandbox:
            print(f"✅ Sandbox criado: {sandbox.sandbox_id}")

            # Configurar ambiente
            if not SandboxManager.setup_sandbox(sandbox):
                raise HTTPException(
                    status_code=500,
                    detail="Falha ao configurar sandbox E2B"
                )

            # Enviar mensagem e obter resposta
            response_text = SandboxManager.send_message(sandbox, req.message)

            return ChatResponse(
                response=response_text,
                sandbox_id=sandbox.sandbox_id,
                model=MINIMAX_CONFIG["model"]
            )

    except HTTPException:
        raise  # Re-raise HTTPException diretamente

    except Exception as e:
        print(f"❌ Erro no endpoint /chat: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar mensagem: {str(e)}"
        )

@router.get("/health", response_model=HealthResponse)
async def health():
    """
    Health check endpoint

    Returns:
        HealthResponse: Status do serviço e modelo configurado
    """
    return HealthResponse(
        status="ok",
        model=MINIMAX_CONFIG["model"]
    )
