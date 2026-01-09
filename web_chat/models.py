from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Mensagem do usuário para o modelo"
    )

class ChatResponse(BaseModel):
    response: str = Field(..., description="Resposta do modelo")
    sandbox_id: str = Field(..., description="ID do sandbox E2B usado")
    model: str = Field(default="minimax/minimax-m2", description="Modelo utilizado")

class HealthResponse(BaseModel):
    status: str = Field(default="ok", description="Status do serviço")
    model: str = Field(..., description="Modelo configurado")
