#!/bin/bash

echo "🚀 Iniciando Claude E2B API Server"
echo "=================================="
echo ""
echo "📍 URLs disponíveis:"
echo "   • Interface Web: http://localhost:8001"
echo "   • API Endpoint:  http://localhost:8001/api/chat"
echo "   • Health Check:  http://localhost:8001/api/health"
echo ""
echo "🔒 Todas as requisições processadas em sandbox E2B isolado"
echo ""
echo "📝 Para expor na rede local, use seu IP:"
echo "   Exemplo: http://$(ipconfig getifaddr en0 2>/dev/null || echo "SEU-IP"):8001"
echo ""
echo "🌍 Para expor na internet, use ngrok:"
echo "   ngrok http 8001"
echo ""
echo "=================================="
echo ""
echo "Pressione Ctrl+C para parar o servidor"
echo ""

python server_web.py
