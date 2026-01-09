# 🌐 Módulo Web Chat - Documentação

## Visão Geral

O módulo `web_chat/` é uma **API REST construída com FastAPI** que expõe o chat com Minimax/Claude via interface HTTP. Fornece:

- 🌐 API REST para chat
- 📄 Interface web HTML/JavaScript
- 🔒 CORS configurável
- ✅ Validação de dados com Pydantic
- 📊 Health check endpoint

---

## 📁 Estrutura de Arquivos

```
web_chat/
├── __init__.py              # Empacotamento do módulo
├── server.py                # Ponto de entrada (uvicorn)
├── app.py                   # Factory da aplicação FastAPI
├── routes.py                # Definição dos endpoints HTTP
├── models.py                # Schemas Pydantic (validação)
└── static/
    └── index.html           # Interface web
```

---

## 📄 server.py - Ponto de Entrada

### Propósito
Script principal para iniciar o servidor web uvicorn.

### Código Completo
```python
#!/usr/bin/env python3
import uvicorn
from claude_mini_sdk.config import SERVER_CONFIG

def main():
    """Inicia servidor web com uvicorn"""
    print("\n" + "=" * 60)
    print("🚀 Claude E2B API - Versão Modular 2.0")
    print("=" * 60)
    print(f"\n📍 Acesse: http://localhost:{SERVER_CONFIG['port']}")
    print("🔒 Sandbox novo a cada request (isolamento total)")
    print("🛡️  CORS configurado (apenas localhost)")
    print("🔑 Token via env var (não hardcoded)")
    print("=" * 60 + "\n")

    uvicorn.run(
        "web_chat.app:app",  # Import path do módulo
        host=SERVER_CONFIG["host"],
        port=SERVER_CONFIG["port"],
        reload=False  # True em desenvolvimento, False em produção
    )

if __name__ == "__main__":
    main()
```

### Responsabilidades
1. Exibir banner informativo no startup
2. Carregar configurações do `claude_mini_sdk.config`
3. Iniciar servidor uvicorn com a aplicação FastAPI

### Como Executar
```bash
# Da raiz do projeto:
python -m web_chat.server

# Ou diretamente:
python web_chat/server.py
```

### Configurações Usadas
- `SERVER_CONFIG["host"]` → `0.0.0.0` (aceita conexões externas)
- `SERVER_CONFIG["port"]` → `8000`
- `reload=False` → Sem auto-reload (use True para dev)

---

## 📄 app.py - Aplicação FastAPI

### Propósito
Cria e configura a instância da aplicação FastAPI com middleware e rotas.

### Código Completo
```python
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
```

### Conceitos

#### 1. Factory Pattern
`create_app()` é uma **factory function** que cria instâncias da aplicação. Vantagens:
- Facilita testes (criar múltiplas instâncias)
- Configuração centralizada
- Flexível para diferentes ambientes

#### 2. CORS (Cross-Origin Resource Sharing)
Controla quais origens podem acessar a API.

**Configuração atual:**
```python
allow_origins=["http://localhost:8000"]  # Apenas localhost
allow_methods=["GET", "POST"]            # Métodos permitidos
allow_headers=["Content-Type"]           # Headers permitidos
```

**Se precisar abrir para outras origens:**
```python
# No claude_mini_sdk/config.py
SERVER_CONFIG = {
    "cors_origins": [
        "http://localhost:8000",
        "http://localhost:3000",  # Frontend React
        "https://meu-site.com"    # Produção
    ]
}
```

#### 3. Router
`app.include_router(router)` registra todas as rotas definidas em `routes.py`.

### Metadata da API
A aplicação expõe documentação automática via FastAPI:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 📄 routes.py - Endpoints HTTP

### Propósito
Define todos os endpoints (rotas) da API REST.

### Endpoints Disponíveis

#### 1. `GET /` - Página Inicial
Serve o arquivo HTML da interface web.

```python
@router.get("/")
async def home():
    """Serve arquivo HTML do frontend"""
    html_path = CURRENT_DIR / "static" / "index.html"
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="index.html não encontrado")
    return FileResponse(html_path)
```

**Response:** Arquivo HTML (Content-Type: text/html)

**Exemplo:**
```bash
curl http://localhost:8000/
# Retorna: HTML da interface
```

---

#### 2. `POST /chat` - Processar Mensagem

Endpoint principal que processa mensagens do usuário.

```python
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
    """
    try:
        # Criar sandbox novo a cada request
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
```

**Request:**
```json
{
  "message": "Qual é a capital do Brasil?"
}
```

**Response (200 OK):**
```json
{
  "response": "A capital do Brasil é Brasília.",
  "sandbox_id": "i9hiosohng0z8yzng3hvr",
  "model": "minimax/minimax-m2"
}
```

**Response (500 Error):**
```json
{
  "detail": "Falha ao configurar sandbox E2B"
}
```

**Exemplo:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá!"}'
```

**Características:**
- ✅ Cria sandbox **novo** a cada request (isolamento total)
- ✅ Validação automática via Pydantic
- ✅ Tratamento de erros com HTTPException
- ✅ Logs detalhados no console
- ⏱️ Pode demorar 10-20s (instalação + API call)

---

#### 3. `GET /health` - Health Check

Endpoint para verificar se a API está online.

```python
@router.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint"""
    return HealthResponse(
        status="ok",
        model=MINIMAX_CONFIG["model"]
    )
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "model": "minimax/minimax-m2"
}
```

**Exemplo:**
```bash
curl http://localhost:8000/health
```

**Uso:**
- Monitoramento (Kubernetes liveness probe)
- Load balancers
- Verificar se servidor está respondendo

---

## 📄 models.py - Schemas Pydantic

### Propósito
Define os **contratos de dados** da API usando Pydantic para validação automática.

### Schemas Definidos

#### 1. ChatRequest
Valida dados de entrada do endpoint `/chat`.

```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """Request para endpoint /chat"""
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Mensagem do usuário para o modelo"
    )
```

**Validações:**
- `message` é obrigatório (`...`)
- Mínimo 1 caractere
- Máximo 5000 caracteres

**Exemplo válido:**
```python
{
  "message": "Olá!"
}
```

**Exemplo inválido (422 Error):**
```python
{
  "message": ""  # Erro: min_length=1
}
```

---

#### 2. ChatResponse
Define estrutura da resposta do endpoint `/chat`.

```python
class ChatResponse(BaseModel):
    """Response do endpoint /chat"""
    response: str = Field(..., description="Resposta do modelo")
    sandbox_id: str = Field(..., description="ID do sandbox E2B usado")
    model: str = Field(default="minimax/minimax-m2", description="Modelo utilizado")
```

**Exemplo:**
```json
{
  "response": "Olá! Como posso ajudar?",
  "sandbox_id": "i9hiosohng0z8yzng3hvr",
  "model": "minimax/minimax-m2"
}
```

---

#### 3. HealthResponse
Define estrutura da resposta do endpoint `/health`.

```python
class HealthResponse(BaseModel):
    """Response do endpoint /health"""
    status: str = Field(default="ok", description="Status do serviço")
    model: str = Field(..., description="Modelo configurado")
```

**Exemplo:**
```json
{
  "status": "ok",
  "model": "minimax/minimax-m2"
}
```

### Benefícios do Pydantic
1. **Validação automática** - FastAPI valida antes de chamar a função
2. **Documentação automática** - Swagger/ReDoc são gerados
3. **Type hints** - Autocomplete na IDE
4. **Serialização** - Conversão automática para JSON

---

## 📄 static/index.html - Interface Web

### Propósito
Interface HTML/JavaScript para interagir com a API via navegador.

### Características

#### 1. Design
- 🎨 Gradiente purple/blue moderno
- 📱 Responsivo (funciona em mobile)
- ✨ Animações e transições suaves

#### 2. Funcionalidades
- ✏️ Textarea para digitar mensagens
- 🔘 Botão "Enviar" (ou Ctrl+Enter)
- ⏳ Spinner de loading durante processamento
- 📝 Renderização de markdown (via marked.js)
- 🎨 Syntax highlighting de código (via highlight.js)

#### 3. Tecnologias
```html
<!-- Bibliotecas externas -->
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
```

#### 4. Fluxo de Uso
1. Usuário digita mensagem no textarea
2. Clica "Enviar" (ou Ctrl+Enter)
3. JavaScript faz `POST /chat` via fetch
4. Mostra spinner enquanto aguarda
5. Resposta é renderizada como markdown
6. Código é highlighted automaticamente

### Exemplo de Interação (JavaScript)
```javascript
async function send() {
    const msg = document.getElementById('msg').value;

    const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
    });

    const data = await res.json();

    // Renderizar markdown
    document.getElementById('content').innerHTML = marked.parse(data.response);
}
```

---

## 🔄 Fluxo Completo de Request

### 1. Cliente Envia Request
```
Browser → POST /chat
Body: {"message": "Olá!"}
```

### 2. FastAPI Recebe
```python
# routes.py
@router.post("/chat")
async def chat(req: ChatRequest):  # Pydantic valida automaticamente
```

### 3. Validação Pydantic
```python
# models.py valida:
- message existe?
- 1 <= len(message) <= 5000?
```

Se falhar → **422 Unprocessable Entity**

### 4. Criar Sandbox
```python
with SandboxManager.create_sandbox() as sandbox:
    # Sandbox criado via claude_mini_sdk/
```

### 5. Setup Sandbox
```python
SandboxManager.setup_sandbox(sandbox)
# Instala Anthropic SDK
```

### 6. Enviar Mensagem
```python
response_text = SandboxManager.send_message(sandbox, "Olá!")
# Executa código no sandbox → chama Minimax API
```

### 7. Retornar Response
```python
return ChatResponse(
    response=response_text,
    sandbox_id=sandbox.sandbox_id,
    model="minimax/minimax-m2"
)
```

### 8. Cliente Recebe
```json
{
  "response": "Olá! Como posso ajudar?",
  "sandbox_id": "...",
  "model": "minimax/minimax-m2"
}
```

### 9. Renderização no Browser
```javascript
// marked.js converte markdown → HTML
content.innerHTML = marked.parse(data.response);
```

---

## 📊 Diagrama de Arquitetura

```
┌──────────────────────────────────────┐
│         Browser (Cliente)            │
│  ┌────────────────────────────────┐  │
│  │  index.html (JavaScript)       │  │
│  └────────────┬───────────────────┘  │
└───────────────┼──────────────────────┘
                │ HTTP POST /chat
                ▼
┌──────────────────────────────────────┐
│      FastAPI (web_chat/)             │
│  ┌────────────────────────────────┐  │
│  │ app.py (FastAPI + CORS)        │  │
│  │   └─> routes.py (Endpoints)    │  │
│  │         └─> models.py (Valid.) │  │
│  └────────────┬───────────────────┘  │
└───────────────┼──────────────────────┘
                │
                ▼
┌──────────────────────────────────────┐
│     claude_mini_sdk/ (Lógica)        │
│  ┌────────────────────────────────┐  │
│  │ SandboxManager.send_message()  │  │
│  │   └─> minimax_client.py        │  │
│  │         └─> utils.py (escape)  │  │
│  └────────────┬───────────────────┘  │
└───────────────┼──────────────────────┘
                │
                ▼
┌──────────────────────────────────────┐
│      E2B Sandbox (Isolado)           │
│  ┌────────────────────────────────┐  │
│  │  Executa código Python:        │  │
│  │  - client.messages.create()    │  │
│  └────────────┬───────────────────┘  │
└───────────────┼──────────────────────┘
                │
                ▼
┌──────────────────────────────────────┐
│      Minimax API                     │
│  ┌────────────────────────────────┐  │
│  │  Modelo: minimax/minimax-m2    │  │
│  │  Retorna: Resposta em PT-BR    │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

---

## 🧪 Testando a API

### 1. Testar Health Check
```bash
curl http://localhost:8000/health
# Resposta: {"status":"ok","model":"minimax/minimax-m2"}
```

### 2. Testar Chat (Terminal)
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Qual é a capital do Brasil?"}'

# Resposta:
# {"response":"A capital do Brasil é Brasília.","sandbox_id":"...","model":"minimax/minimax-m2"}
```

### 3. Testar Chat (Python)
```python
import requests

response = requests.post('http://localhost:8000/chat', json={
    'message': 'Olá!'
})

print(response.json())
# {'response': 'Olá! Como posso ajudar?', ...}
```

### 4. Testar Interface Web
```bash
# Abrir no navegador:
open http://localhost:8000
```

### 5. Testar Documentação Automática
```bash
# Swagger UI:
open http://localhost:8000/docs

# ReDoc:
open http://localhost:8000/redoc
```

---

## 🔧 Configurações e Personalizações

### 1. Mudar Porta
```python
# claude_mini_sdk/config.py
SERVER_CONFIG = {
    "port": 3000  # Ao invés de 8000
}
```

### 2. Habilitar Auto-reload (Dev)
```python
# web_chat/server.py
uvicorn.run(
    "web_chat.app:app",
    reload=True  # Auto-restart ao salvar arquivos
)
```

### 3. Adicionar Logging
```python
# web_chat/app.py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Em routes.py:
logger.info(f"Mensagem recebida: {req.message}")
```

### 4. Ajustar CORS
```python
# claude_mini_sdk/config.py
SERVER_CONFIG = {
    "cors_origins": [
        "http://localhost:8000",
        "http://localhost:3000",  # React app
        "*"  # Permitir todas (não recomendado em produção)
    ]
}
```

### 5. Aumentar max_tokens
```python
# claude_mini_sdk/config.py
MINIMAX_CONFIG = {
    "max_tokens": 2000  # Ao invés de 800
}
```

---

## 🚀 Deploy em Produção

### 1. Variáveis de Ambiente
Nunca commitar `.env`! Em produção, configurar:
```bash
export MINIMAX_TOKEN="sk-cp-..."
export E2B_API_KEY="e2b_..."
```

### 2. Usar Gunicorn (Multi-workers)
```bash
pip install gunicorn
gunicorn web_chat.app:app -w 4 -k uvicorn.workers.UvicornWorker
```

### 3. Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name api.meusite.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
    }
}
```

### 4. Docker
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "web_chat.server"]
```

---

## 🔍 Troubleshooting

### Erro: "Address already in use"
**Causa:** Porta 8000 ocupada
**Solução:**
```bash
lsof -ti:8000 | xargs kill -9
```

### Erro: "CORS error" no browser
**Causa:** Origem não permitida
**Solução:** Adicionar origem em `SERVER_CONFIG["cors_origins"]`

### Erro: "422 Unprocessable Entity"
**Causa:** Dados inválidos (ex: message vazio)
**Solução:** Verificar validação em `models.py`

### Erro: "500 Internal Server Error"
**Causa:** Falha no sandbox ou API
**Solução:** Ver logs do servidor para detalhes

---

## 📚 Referências

### FastAPI
- [Docs Oficiais](https://fastapi.tiangolo.com/)
- [Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Advanced User Guide](https://fastapi.tiangolo.com/advanced/)

### Pydantic
- [Docs](https://docs.pydantic.dev/)
- [Field Validation](https://docs.pydantic.dev/latest/concepts/fields/)

### Uvicorn
- [Docs](https://www.uvicorn.org/)
- [Deployment](https://www.uvicorn.org/deployment/)

---

## 📝 Próximos Passos

Para aprofundar:

1. **Adicionar testes** - pytest + TestClient
2. **Rate limiting** - Limitar requests por IP
3. **Authentication** - JWT tokens
4. **Streaming** - Respostas em tempo real
5. **WebSockets** - Chat bidirecional
6. **Cache** - Redis para respostas frequentes
7. **Métricas** - Prometheus + Grafana

Boa sorte nos estudos! 🚀
