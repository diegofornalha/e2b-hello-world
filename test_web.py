#!/usr/bin/env python3
"""
Teste rápido da API web
"""
import requests
import time

print("🧪 Testando API Web do Claude E2B...")
print("="*60)

url = "http://localhost:8001/api/chat"

print(f"\n📍 URL: {url}")
print(f"📝 Mensagem: 'Oi'")
print(f"\n⏳ Aguardando resposta (pode demorar 10-20s na primeira vez)...\n")

start = time.time()

try:
    response = requests.post(
        url,
        json={"message": "Oi", "max_tokens": 200},
        timeout=120
    )

    elapsed = time.time() - start

    if response.status_code == 200:
        data = response.json()
        print("="*60)
        print("✅ SUCESSO!")
        print("="*60)
        print(f"\n{data['response']}\n")
        print("="*60)
        print(f"⏱️  Tempo: {elapsed:.1f}s")
        print(f"🆔 Sandbox: {data['sandbox_id']}")
        print(f"🤖 Modelo: {data['model']}")
        print("="*60)
    else:
        print(f"❌ Erro {response.status_code}: {response.text}")

except requests.exceptions.Timeout:
    print("❌ Timeout - Servidor demorou muito para responder")
except Exception as e:
    print(f"❌ Erro: {e}")
