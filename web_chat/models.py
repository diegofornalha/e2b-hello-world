"""
Schemas Pydantic para validação de request/response

Define os contratos da API HTTP com validação automática.
"""

from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """Request para endpoint /chat"""
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Mensagem do usuário para o modelo"
    )

class ChatResponse(BaseModel):
    """Response do endpoint /chat"""
    response: str = Field(..., description="Resposta do modelo")
    sandbox_id: str = Field(..., description="ID do sandbox E2B usado")
    model: str = Field(default="minimax/minimax-m2", description="Modelo utilizado")

class HealthResponse(BaseModel):
    """Response do endpoint /health"""
    status: str = Field(default="ok", description="Status do serviço")
    model: str = Field(..., description="Modelo configurado")
