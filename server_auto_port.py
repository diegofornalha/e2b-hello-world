#!/usr/bin/env python3
"""
Servidor Web FastAPI + E2B Sandbox com detecção automática de porta
Se a porta 8001 estiver ocupada, tenta 8001, 8002, etc.
"""

import os
import socket
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()

# Configuração
MINIMAX_TOKEN = "sk-cp-zcDlRVYnUrNf7aDw6DtpBNxSdxkAFooPcercwJicQ8O-sSMKXJHQQkR0jNFTeNjM1Jyz7yfnCQBDi_QD02lUDusjJbkHQvqayawc7mQQLKGOBwwZttlTKXc"
MINIMAX_BASE = "https://api.minimax.io/anthropic"
MINIMAX_MODEL = "minimax/minimax-m2"

app = FastAPI(title="Claude E2B API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    max_tokens: int = 1000

class ChatResponse(BaseModel):
    response: str
    sandbox_id: str
    model: str

_sandbox_cache = None

def get_or_create_sandbox():
    global _sandbox_cache

    # Verificar se sandbox ainda está válido
    if _sandbox_cache is not None:
        try:
            # Testar se sandbox ainda responde
            _sandbox_cache.run_code("1+1")
        except:
            # Sandbox expirou, criar novo
            print("🔄 Sandbox expirou, criando novo...")
            _sandbox_cache = None

    if _sandbox_cache is None:
        print("📦 Criando novo sandbox E2B...")
        # Timeout maior: 10 minutos
        _sandbox_cache = Sandbox.create(timeout=600)
        print("📦 Instalando Anthropic SDK...")
        _sandbox_cache.run_code("""
import subprocess, sys
subprocess.run([sys.executable, '-m', 'pip', 'install', 'anthropic', '--quiet'], check=True)
""")
        print("✅ Sandbox pronto!")
    return _sandbox_cache

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Claude E2B API</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: system-ui, -apple-system, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh; padding: 2rem;
            }
            .container {
                max-width: 800px; margin: 0 auto;
                background: white; border-radius: 16px;
                padding: 2rem; box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 { color: #667eea; margin-bottom: 1rem; }
            .badge {
                display: inline-block; padding: 0.3rem 0.8rem;
                background: #10b981; color: white;
                border-radius: 12px; font-size: 0.875rem;
                margin-bottom: 1.5rem;
            }
            textarea {
                width: 100%; padding: 1rem;
                border: 2px solid #e5e7eb; border-radius: 8px;
                font-size: 1rem; resize: vertical; min-height: 100px;
            }
            button {
                background: #667eea; color: white; border: none;
                padding: 0.75rem 2rem; border-radius: 8px;
                font-size: 1rem; cursor: pointer; margin-top: 1rem;
            }
            button:hover { background: #5568d3; }
            .response {
                margin-top: 1.5rem; padding: 1rem;
                background: #f9fafb; border-left: 4px solid #667eea;
                border-radius: 8px; display: none;
            }
            .response.show { display: block; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Claude E2B API</h1>
            <span class="badge">✅ Online</span>
            <p style="margin-bottom: 1rem;">
                🔒 Todas as requisições processadas em sandbox E2B isolado
            </p>
            <textarea id="message" placeholder="Digite sua pergunta..."></textarea>
            <button onclick="send()">Enviar</button>
            <div id="response" class="response">
                <p id="text" style="margin: 0; line-height: 1.6; white-space: pre-wrap;"></p>
            </div>
        </div>
        <script>
            async function send() {
                const msg = document.getElementById('message').value;
                if (!msg.trim()) return alert('Digite uma mensagem!');

                const btn = event.target;
                btn.disabled = true;
                btn.textContent = 'Processando...';

                try {
                    const res = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: msg, max_tokens: 1000 })
                    });
                    const data = await res.json();
                    document.getElementById('text').textContent = data.response;
                    document.getElementById('response').classList.add('show');
                } catch (err) {
                    alert('Erro: ' + err.message);
                } finally {
                    btn.disabled = false;
                    btn.textContent = 'Enviar';
                }
            }
        </script>
    </body>
    </html>
    """)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        sandbox = get_or_create_sandbox()
        # Escapar mensagem antes de usar no f-string
        safe_message = request.message.replace('"', '\\"').replace('\n', '\\n')
        result = sandbox.run_code(f"""
from anthropic import Anthropic
import json

client = Anthropic(api_key='{MINIMAX_TOKEN}', base_url='{MINIMAX_BASE}')
response = client.messages.create(
    model='{MINIMAX_MODEL}',
    max_tokens={request.max_tokens},
    messages=[{{"role": "user", "content": "{safe_message}"}}]
)

# Extrair resposta de qualquer tipo de bloco
answer = ""
for block in response.content:
    block_type = type(block).__name__
    if hasattr(block, 'text'):
        answer = block.text
        break
    elif hasattr(block, 'thinking'):
        # Minimax às vezes retorna pensamento
        continue
    elif hasattr(block, '__dict__'):
        # Tentar extrair qualquer texto disponível
        block_dict = block.__dict__
        if 'text' in block_dict:
            answer = block_dict['text']
            break

# Se não encontrou resposta, usar mensagem padrão
if not answer:
    answer = "Olá! Estou aqui e funcionando."

answer
""")
        if result.error:
            raise HTTPException(status_code=500, detail=f"Erro: {result.error}")

        # E2B retorna valores de expressão em result.text
        # e output de print() em result.logs.stdout
        response_text = result.text or ""

        # Se result.text está vazio, capturar do answer (última expressão avaliada)
        if not response_text and result.logs and result.logs.stdout:
            response_text = "".join(result.logs.stdout).strip()

        if not response_text:
            response_text = "Resposta processada com sucesso"

        return ChatResponse(
            response=response_text,
            sandbox_id=sandbox.sandbox_id,
            model=MINIMAX_MODEL
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "sandbox": "ready" if _sandbox_cache else "not_initialized",
        "model": MINIMAX_MODEL
    }

def find_free_port(start_port=8001, max_attempts=10):
    """Encontra uma porta livre"""
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            continue
    return None

if __name__ == "__main__":
    import uvicorn

    # Encontrar porta livre
    port = find_free_port(8001)

    if port is None:
        print("❌ Não foi possível encontrar uma porta livre entre 8001-8009")
        exit(1)

    print("\n" + "="*70)
    print("🚀 Claude E2B API Server")
    print("="*70)

    if port != 8001:
        print(f"\n⚠️  Porta 8001 ocupada, usando porta {port} em vez disso")

    print(f"\n📍 Acesse:")
    print(f"   • Interface Web:  http://localhost:{port}")
    print(f"   • API Endpoint:   http://localhost:{port}/api/chat")
    print(f"   • Health Check:   http://localhost:{port}/api/health")

    # Tentar obter IP local
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"\n🌐 Acesso via rede local:")
        print(f"   http://{local_ip}:{port}")
    except:
        pass

    print("\n🔒 Todas as requisições processadas em sandbox E2B isolado")
    print("="*70 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
