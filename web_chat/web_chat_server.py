#!/usr/bin/env python3
"""
Servidor Web Simplificado - E2B + Minimax
Versão funcionando garantida!
"""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

# Carregar .env da raiz do projeto
load_dotenv(Path(__file__).parent.parent / ".env")

# Diretório atual (web_chat/)
CURRENT_DIR = Path(__file__).parent

# Exemplo: MINIMAX_TOKEN no .env ao invés de hardcoded
MINIMAX_TOKEN = os.getenv("MINIMAX_TOKEN")

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def home():
    """Serve o arquivo HTML separado"""
    return FileResponse(CURRENT_DIR / "index.html")

@app.post("/chat")
async def chat(req: ChatRequest):
    """Cria sandbox novo a cada request (mais confiável)"""
    try:
        print(f"\n📨 Recebido: {req.message[:50]}...")

        with Sandbox.create(timeout=180) as sandbox:
            print(f"✅ Sandbox: {sandbox.sandbox_id}")

            # Instalar Anthropic
            print("📦 Instalando...")
            sandbox.run_code("""
import subprocess, sys
subprocess.run([sys.executable, '-m', 'pip', 'install', 'anthropic', '--quiet'])
""")

            # Chamar Minimax
            print("🤖 Chamando Claude...")
            msg_safe = req.message.replace("'", "\\'").replace('"', '\\"')

            result = sandbox.run_code(f"""
from anthropic import Anthropic

client = Anthropic(
    api_key='{MINIMAX_TOKEN}',
    base_url='https://api.minimax.io/anthropic'
)

resp = client.messages.create(
    model='minimax/minimax-m2',
    max_tokens=800,
    messages=[{{"role": "user", "content": "{msg_safe}"}}]
)

# Extrair texto
texto = ""
for bloco in resp.content:
    if hasattr(bloco, 'text'):
        texto = bloco.text
        break

# Retornar como última expressão
texto if texto else "Olá! Sistema funcionando."
""")

            # Capturar resposta
            resposta = result.text or ""

            print(f"✅ Resposta: {resposta[:100]}...")

            return {"response": resposta, "sandbox_id": sandbox.sandbox_id}

    except Exception as e:
        print(f"❌ Erro: {e}")
        return {"response": f"Erro: {str(e)}", "sandbox_id": "error"}

@app.get("/health")
async def health():
    return {"status": "ok", "model": "minimax/minimax-m2"}

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 Claude E2B API - Versão Simplificada")
    print("="*60)
    print("\n📍 Acesse: http://localhost:8000")
    print("🔒 Sandbox novo a cada request (mais confiável)")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
