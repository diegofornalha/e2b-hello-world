#!/usr/bin/env python3
"""
Servidor Web FastAPI + E2B Sandbox
Expõe Claude/Minimax via HTTP API

Arquitetura:
┌─────────────────────────┐
│  Cliente (Browser)      │
│  http://localhost:8001  │
└───────────┬─────────────┘
            │ HTTP
            ▼
┌─────────────────────────┐
│  FastAPI Server         │
│  (seu computador)       │
└───────────┬─────────────┘
            │ E2B API
            ▼
┌─────────────────────────┐
│  E2B Cloud Sandbox      │
│  ┌───────────────────┐  │
│  │ Claude/Minimax    │  │
│  └───────────────────┘  │
└─────────────────────────┘
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox
import json

load_dotenv()

# Configuração
MINIMAX_TOKEN = "sk-cp-zcDlRVYnUrNf7aDw6DtpBNxSdxkAFooPcercwJicQ8O-sSMKXJHQQkR0jNFTeNjM1Jyz7yfnCQBDi_QD02lUDusjJbkHQvqayawc7mQQLKGOBwwZttlTKXc"
MINIMAX_BASE = "https://api.minimax.io/anthropic"
MINIMAX_MODEL = "minimax/minimax-m2"

# FastAPI App
app = FastAPI(
    title="Claude E2B API",
    description="API que expõe Claude/Minimax rodando em sandbox E2B isolado",
    version="1.0.0"
)

# CORS (permitir requisições de qualquer origem)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de dados
class ChatRequest(BaseModel):
    message: str
    max_tokens: int = 1000

class ChatResponse(BaseModel):
    response: str
    sandbox_id: str
    model: str

# Cache de sandbox (reutilizar para múltiplas requests)
_sandbox_cache = None

def get_or_create_sandbox():
    """
    Cria ou reutiliza sandbox E2B
    """
    global _sandbox_cache

    if _sandbox_cache is None:
        print("📦 Criando novo sandbox E2B...")
        _sandbox_cache = Sandbox.create()

        # Setup inicial: instalar Anthropic SDK
        print("📦 Instalando Anthropic SDK...")
        _sandbox_cache.run_code("""
import subprocess
import sys
subprocess.run([sys.executable, '-m', 'pip', 'install', 'anthropic', '--quiet'], check=True)
""")
        print("✅ Sandbox pronto!")

    return _sandbox_cache

@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Página inicial com interface de teste
    """
    html = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Claude E2B API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 2rem;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                border-radius: 16px;
                padding: 2rem;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                margin-bottom: 0.5rem;
            }
            .badge {
                display: inline-block;
                padding: 0.25rem 0.75rem;
                background: #10b981;
                color: white;
                border-radius: 12px;
                font-size: 0.875rem;
                margin-bottom: 1.5rem;
            }
            .info {
                background: #f3f4f6;
                padding: 1rem;
                border-radius: 8px;
                margin-bottom: 1.5rem;
            }
            .info p {
                margin: 0.5rem 0;
                font-size: 0.875rem;
            }
            textarea {
                width: 100%;
                padding: 1rem;
                border: 2px solid #e5e7eb;
                border-radius: 8px;
                font-size: 1rem;
                resize: vertical;
                min-height: 100px;
                font-family: inherit;
            }
            textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                background: #667eea;
                color: white;
                border: none;
                padding: 0.75rem 2rem;
                border-radius: 8px;
                font-size: 1rem;
                cursor: pointer;
                margin-top: 1rem;
                transition: all 0.2s;
            }
            button:hover {
                background: #5568d3;
                transform: translateY(-2px);
            }
            button:disabled {
                background: #9ca3af;
                cursor: not-allowed;
                transform: none;
            }
            .response {
                margin-top: 1.5rem;
                padding: 1rem;
                background: #f9fafb;
                border-left: 4px solid #667eea;
                border-radius: 8px;
                display: none;
            }
            .response.show {
                display: block;
            }
            .loading {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid rgba(255,255,255,.3);
                border-radius: 50%;
                border-top-color: white;
                animation: spin 1s ease-in-out infinite;
            }
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Claude E2B API</h1>
            <span class="badge">✅ Online</span>

            <div class="info">
                <p><strong>🔒 Isolamento:</strong> Todas as requisições são processadas em sandbox E2B isolado</p>
                <p><strong>🤖 Modelo:</strong> Minimax M2 (proxy Anthropic)</p>
                <p><strong>📍 Endpoint:</strong> POST /api/chat</p>
            </div>

            <label for="message"><strong>💬 Sua mensagem:</strong></label>
            <textarea id="message" placeholder="Digite sua pergunta aqui..."></textarea>

            <button id="sendBtn" onclick="sendMessage()">
                Enviar Mensagem
            </button>

            <div id="response" class="response">
                <strong>🤖 Resposta do Claude:</strong>
                <p id="responseText"></p>
                <small id="responseInfo" style="color: #6b7280; margin-top: 0.5rem; display: block;"></small>
            </div>
        </div>

        <script>
            async function sendMessage() {
                const message = document.getElementById('message').value;
                const btn = document.getElementById('sendBtn');
                const responseDiv = document.getElementById('response');
                const responseText = document.getElementById('responseText');
                const responseInfo = document.getElementById('responseInfo');

                if (!message.trim()) {
                    alert('Por favor, digite uma mensagem!');
                    return;
                }

                // Loading state
                btn.disabled = true;
                btn.innerHTML = '<span class="loading"></span> Processando...';
                responseDiv.classList.remove('show');

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message, max_tokens: 1000 })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        responseText.textContent = data.response;
                        responseInfo.textContent = `Sandbox: ${data.sandbox_id} | Modelo: ${data.model}`;
                        responseDiv.classList.add('show');
                    } else {
                        alert('Erro: ' + (data.detail || 'Erro desconhecido'));
                    }
                } catch (error) {
                    alert('Erro na requisição: ' + error.message);
                } finally {
                    btn.disabled = false;
                    btn.innerHTML = 'Enviar Mensagem';
                }
            }

            // Enter para enviar
            document.getElementById('message').addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal: envia mensagem para Claude no E2B
    """
    try:
        sandbox = get_or_create_sandbox()

        # Executar no sandbox
        result = sandbox.run_code(f"""
from anthropic import Anthropic

client = Anthropic(
    api_key='{MINIMAX_TOKEN}',
    base_url='{MINIMAX_BASE}'
)

response = client.messages.create(
    model='{MINIMAX_MODEL}',
    max_tokens={request.max_tokens},
    messages=[{{"role": "user", "content": "{request.message.replace('"', '\\"')}"}}]
)

# Extrair resposta
answer = ""
for block in response.content:
    if hasattr(block, 'text'):
        answer = block.text
        break

print(answer)
""")

        if result.error:
            raise HTTPException(status_code=500, detail=f"Erro no sandbox: {result.error}")

        return ChatResponse(
            response=result.text or "Resposta processada com sucesso",
            sandbox_id=sandbox.sandbox_id,
            model=MINIMAX_MODEL
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "sandbox": "ready" if _sandbox_cache else "not_initialized",
        "model": MINIMAX_MODEL
    }

@app.on_event("shutdown")
async def shutdown():
    """
    Limpar recursos ao desligar
    """
    global _sandbox_cache
    if _sandbox_cache:
        print("🗑️  Fechando sandbox...")
        _sandbox_cache.close()
        _sandbox_cache = None

if __name__ == "__main__":
    import uvicorn

    print("\n" + "="*60)
    print("🚀 Iniciando Claude E2B API Server")
    print("="*60)
    print("\n📍 Acesse:")
    print("   • Interface Web: http://localhost:8001")
    print("   • API Endpoint:  http://localhost:8001/api/chat")
    print("   • Health Check:  http://localhost:8001/api/health")
    print("\n🔒 Todas as requisições processadas em sandbox E2B isolado")
    print("="*60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
