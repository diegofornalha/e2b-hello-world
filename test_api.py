#!/usr/bin/env python3
import requests
import time

print("🧪 Testando API do servidor...\n")
print("📍 URL: http://localhost:8000/chat")
print("📝 Mensagem: 'Oi, você está funcionando?'")
print("\n⏳ Aguardando resposta (pode demorar 15-25s na primeira chamada)...\n")

start = time.time()

try:
    response = requests.post(
        "http://localhost:8000/chat",
        json={"message": "Oi, você está funcionando?"},
        timeout=120
    )

    elapsed = time.time() - start

    print("="*60)
    if response.status_code == 200:
        data = response.json()
        print("✅ SUCESSO!")
        print("="*60)
        print(f"\n🤖 RESPOSTA:\n{data['response']}\n")
        print("="*60)
        print(f"⏱️  Tempo: {elapsed:.1f}s")
        print(f"🆔 Sandbox: {data['sandbox_id']}")
        print("="*60)
    else:
        print(f"❌ Erro {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"❌ Erro: {e}")
