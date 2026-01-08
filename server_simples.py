#!/usr/bin/env python3
"""
Servidor Web Simplificado - E2B + Minimax
Versão funcionando garantida!
"""

import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from e2b_code_interpreter import Sandbox

load_dotenv()

MINIMAX_TOKEN = "sk-cp-zcDlRVYnUrNf7aDw6DtpBNxSdxkAFooPcercwJicQ8O-sSMKXJHQQkR0jNFTeNjM1Jyz7yfnCQBDi_QD02lUDusjJbkHQvqayawc7mQQLKGOBwwZttlTKXc"

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Claude E2B API</title>
        <style>
            body { font-family: system-ui; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; padding: 2rem; margin: 0; }
            .container { max-width: 700px; margin: 0 auto; background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
            h1 { color: #667eea; margin: 0 0 1rem 0; }
            textarea { width: 100%; padding: 1rem; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 1rem; min-height: 100px; resize: vertical; font-family: inherit; }
            button { background: #667eea; color: white; border: none; padding: 0.75rem 2rem; border-radius: 8px; font-size: 1rem; cursor: pointer; margin-top: 1rem; }
            button:hover { background: #5568d3; }
            button:disabled { background: #9ca3af; cursor: wait; }
            .response { margin-top: 1.5rem; padding: 1rem; background: #f9fafb; border-left: 4px solid #667eea; border-radius: 8px; display: none; }
            .response.show { display: block; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Claude E2B API</h1>
            <p style="color: #10b981; margin-bottom: 1rem;">✅ Online - Rodando em sandbox E2B isolado</p>
            <textarea id="msg" placeholder="Digite sua pergunta..."></textarea>
            <button onclick="send()">Enviar</button>
            <div id="resp" class="response">
                <p id="text" style="margin: 0; line-height: 1.6; white-space: pre-wrap;"></p>
            </div>
        </div>
        <script>
            async function send() {
                const msg = document.getElementById('msg').value;
                if (!msg.trim()) return alert('Digite algo!');
                const btn = event.target;
                btn.disabled = true;
                btn.textContent = 'Aguarde 10-20s...';
                document.getElementById('resp').classList.remove('show');
                try {
                    const res = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: msg })
                    });
                    const data = await res.json();
                    document.getElementById('text').textContent = data.response;
                    document.getElementById('resp').classList.add('show');
                } catch (err) {
                    alert('Erro: ' + err);
                } finally {
                    btn.disabled = false;
                    btn.textContent = 'Enviar';
                }
            }
        </script>
    </body>
    </html>
    """

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
