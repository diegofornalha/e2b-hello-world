# 🌐 Servidor Web com E2B Sandbox

## 🎯 O que foi criado?

Um **servidor HTTP** que expõe o Claude/Minimax rodando no E2B Sandbox via API REST.

```
Internet/Rede Local
        │
        ▼
┌──────────────────────┐
│  http://seu-ip:8001  │  ← Acesso via browser/API
└──────────┬───────────┘
           │ HTTP
           ▼
┌──────────────────────┐
│  FastAPI Server      │  ← Roda no seu computador
│  (server_web.py)     │
└──────────┬───────────┘
           │ E2B API
           ▼
┌──────────────────────┐
│  E2B Cloud Sandbox   │  ← Isolado na nuvem
│  ┌────────────────┐  │
│  │ Claude/Minimax │  │
│  └────────────────┘  │
└──────────────────────┘
```

---

## 🚀 Como Usar

### 1. Instalar dependências adicionais

```bash
pip install -r requirements_server.txt
```

### 2. Iniciar servidor

```bash
python server_web.py
```

### 3. Acessar

```bash
# Interface Web (Browser)
http://localhost:8001

# API direta (curl/Postman)
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá, Claude!"}'

# Health Check
curl http://localhost:8001/api/health
```

---

## 🌍 Expor para Internet/Rede

### Opção 1: Rede Local (LAN)

```bash
# O servidor já está configurado para aceitar conexões externas (0.0.0.0)
# Descubra seu IP local:
ifconfig | grep "inet " | grep -v 127.0.0.1

# Exemplo: 192.168.1.100
# Outros dispositivos na mesma rede acessam:
http://192.168.1.100:8001
```

### Opção 2: Ngrok (Túnel público temporário)

```bash
# 1. Instalar ngrok
brew install ngrok
# ou baixar de: https://ngrok.com/download

# 2. Iniciar servidor (terminal 1)
python server_web.py

# 3. Criar túnel (terminal 2)
ngrok http 8001

# Output:
# Forwarding: https://abc123.ngrok.io -> http://localhost:8001
```

**Agora qualquer um pode acessar:**
```
https://abc123.ngrok.io
```

### Opção 3: Cloudflare Tunnel (Grátis, permanente)

```bash
# 1. Instalar cloudflared
brew install cloudflared

# 2. Login no Cloudflare
cloudflared tunnel login

# 3. Criar túnel
cloudflared tunnel create claude-e2b-api

# 4. Configurar (criar config.yml)
# 5. Rodar túnel
cloudflared tunnel run claude-e2b-api
```

### Opção 4: Deploy em Cloud (Produção)

#### **Render.com** (Recomendado - Fácil)
```yaml
# render.yaml
services:
  - type: web
    name: claude-e2b-api
    env: python
    buildCommand: "pip install -r requirements_server.txt"
    startCommand: "python server_web.py"
    envVars:
      - key: E2B_API_KEY
        sync: false
```

Deploy:
```bash
git init
git add .
git commit -m "Deploy Claude E2B API"
# Conectar ao Render.com via interface web
```

#### **Fly.io**
```bash
fly launch
fly deploy
```

#### **Railway.app**
```bash
railway login
railway init
railway up
```

---

## 📡 Endpoints Disponíveis

### 1. Interface Web
```
GET /
```
Interface visual para testar a API

### 2. Chat API
```
POST /api/chat
Content-Type: application/json

{
  "message": "Sua pergunta aqui",
  "max_tokens": 1000
}
```

**Resposta:**
```json
{
  "response": "Resposta do Claude...",
  "sandbox_id": "i4no066iuu0x...",
  "model": "minimax/minimax-m2"
}
```

### 3. Health Check
```
GET /api/health
```

**Resposta:**
```json
{
  "status": "healthy",
  "sandbox": "ready",
  "model": "minimax/minimax-m2"
}
```

---

## 🔐 Segurança

### Atual (Desenvolvimento)
- ⚠️ Sem autenticação
- ⚠️ CORS aberto (`allow_origins=["*"]`)
- ⚠️ API key hardcoded

### Para Produção (Adicionar)

```python
# 1. Autenticação com API Key
from fastapi import Header, HTTPException

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv("API_SECRET_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API Key")

@app.post("/api/chat", dependencies=[Depends(verify_api_key)])
async def chat(request: ChatRequest):
    ...

# 2. Rate Limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: Request, chat_request: ChatRequest):
    ...

# 3. HTTPS (com Nginx/Cloudflare)
# 4. Variáveis de ambiente (nunca hardcode!)
```

---

## 💰 Custos

| Serviço | Custo | Nota |
|---------|-------|------|
| **E2B** | Varia | Tier gratuito disponível |
| **Minimax API** | Por uso | Depende das chamadas |
| **Ngrok** | Grátis (túnel temporário) | URL muda a cada restart |
| **Cloudflare Tunnel** | Grátis | Permanente |
| **Render.com** | Grátis (com sleep) | $7/mês para sempre online |
| **Fly.io** | Grátis (limite) | Pay-as-you-go depois |

---

## 🧪 Testar a API

### Com curl
```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explique o que é E2B Sandbox",
    "max_tokens": 500
  }'
```

### Com Python
```python
import requests

response = requests.post(
    "http://localhost:8001/api/chat",
    json={"message": "Olá, Claude!", "max_tokens": 500}
)

print(response.json()["response"])
```

### Com JavaScript (Frontend)
```javascript
fetch('http://localhost:8001/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: 'Olá, Claude!',
    max_tokens: 500
  })
})
.then(r => r.json())
.then(data => console.log(data.response))
```

---

## 🎨 Customizações

### Adicionar Streaming (Server-Sent Events)

```python
@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    async def event_generator():
        sandbox = get_or_create_sandbox()

        # Usar streaming do Anthropic
        result = sandbox.run_code(f"""
from anthropic import Anthropic

client = Anthropic(...)
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end='', flush=True)
""")

        for chunk in result.text:
            yield f"data: {chunk}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

### Adicionar WebSocket (Chat em tempo real)

```python
from fastapi import WebSocket

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    sandbox = get_or_create_sandbox()

    while True:
        message = await websocket.receive_text()
        # Processar no E2B
        response = process_in_sandbox(sandbox, message)
        await websocket.send_text(response)
```

---

## 📊 Monitoramento

Adicionar logs estruturados:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/api/chat")
async def chat(request: ChatRequest):
    logger.info(f"Received message: {request.message[:50]}...")
    # ...
    logger.info(f"Responded in {elapsed_time}s")
```

---

## 🆘 Troubleshooting

### Erro: "Address already in use"
```bash
# Porta 8001 já está em uso
# Trocar porta:
uvicorn server_web:app --port 8001
```

### Erro: "Sandbox timeout"
```bash
# Aumentar timeout do E2B
sandbox = Sandbox.create(timeout=300)
```

### Erro: "Connection refused" (rede externa)
```bash
# Verificar firewall
sudo ufw allow 8001

# macOS: Permitir conexões no Firewall
```

---

## 📚 Próximos Passos

1. ✅ Servidor funcionando localmente
2. 🔄 Testar com ngrok (acesso público)
3. 🔐 Adicionar autenticação
4. 📊 Implementar rate limiting
5. 🚀 Deploy em produção
6. 🔔 Adicionar webhooks
7. 📈 Métricas e analytics

---

**Criado por:** Claude Code + E2B + FastAPI
