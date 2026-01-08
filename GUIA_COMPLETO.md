# 🚀 Guia Completo: Claude/Minimax no E2B Sandbox

## 📋 Índice
1. [O que é E2B e por que usar?](#o-que-é-e2b)
2. [Segurança e Isolamento](#segurança-e-isolamento)
3. [Scripts Disponíveis](#scripts-disponíveis)
4. [Como Executar](#como-executar)
5. [Arquitetura](#arquitetura)

---

## 🔐 O que é E2B?

**E2B** (Execution in Elastic Box) é um provedor de **sandboxes isolados na nuvem**.

### Por que usar E2B?

| Benefício | Explicação |
|-----------|------------|
| 🛡️ **Isolamento Total** | Código roda separado do seu computador |
| 🔒 **Proteção de Segredos** | Dados de produção nunca expostos |
| 📦 **Ambiente Limpo** | Cada sandbox é novo e destruído após uso |
| ☁️ **Cloud Native** | Escalável e gerenciado |
| 🚀 **Rápido** | Containers otimizados |

---

## 🛡️ Segurança e Isolamento

### O que o sandbox E2B **NÃO PODE** acessar:

```
❌ Arquivos do seu computador
❌ Suas variáveis de ambiente locais
❌ Rede local (192.168.x.x)
❌ Outros processos da sua máquina
❌ Permanecer ativo após encerrar
```

### Como funciona o isolamento:

```
┌─────────────────────────────────────┐
│  SEU COMPUTADOR                     │
│                                     │
│  📂 /Users/seu-usuario/            │
│  🔐 Segredos de produção           │
│  💻 Sistema operacional            │
│                                     │
│  [Script Python]                   │
│       │                            │
│       │ Envia apenas:              │
│       │ • Código para executar     │
│       │ • Variáveis específicas    │
│       │                            │
└───────┼─────────────────────────────┘
        │
        │ HTTPS (API E2B)
        │
        ▼
┌─────────────────────────────────────┐
│  NUVEM E2B                          │
│  ┌───────────────────────────────┐  │
│  │  Container Docker Isolado     │  │
│  │                               │  │
│  │  • Filesystem próprio         │  │
│  │  • Rede isolada               │  │
│  │  • Recursos limitados         │  │
│  │  • Auto-destruição            │  │
│  │                               │  │
│  │  [Anthropic SDK]              │  │
│  │  [Minimax API]                │  │
│  │                               │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Analogia simples:

Imagine que você quer testar um código "suspeito". Em vez de rodar no seu computador (arriscado), você:

1. **Manda o código** para uma máquina virtual descartável na nuvem (E2B)
2. **Código executa** lá, isolado
3. **Recebe apenas o resultado** de volta
4. **Máquina virtual é destruída** automaticamente

Seu computador **nunca** executou o código diretamente!

---

## 📦 Scripts Disponíveis

### 1. `hello_world.py` - Teste Básico E2B

**Propósito:** Testar se E2B está funcionando

```bash
python hello_world.py
```

**O que faz:**
- ✅ Cria sandbox E2B
- ✅ Executa 4 testes matemáticos
- ✅ Verifica informações do sistema
- ✅ Fecha sandbox

**Tempo:** ~10 segundos

---

### 2. `agent_in_sandbox.py` - Claude Agent SDK Padrão

**Propósito:** Testar Claude SDK padrão (Anthropic oficial)

```bash
python agent_in_sandbox.py
```

**Requer:**
- E2B_API_KEY
- ANTHROPIC_API_KEY (oficial)

**O que faz:**
- Instala Anthropic SDK no sandbox
- Executa 2 tarefas de exemplo
- Demonstra isolamento

---

### 3. `run_assistente_in_sandbox.py` - Minimax API

**Propósito:** Rodar com credenciais Minimax (proxy Anthropic)

```bash
python run_assistente_in_sandbox.py
```

**Configuração:**
- Usa Minimax como proxy da Anthropic
- Base URL: `https://api.minimax.io/anthropic`
- Modelo: `minimax/minimax-m2`

**O que faz:**
- Configura env vars customizadas
- Instala dependências
- Testa conexão com Minimax
- Executa tarefa sobre Data Lake

---

### 4. `chat_minimax_in_sandbox.py` ⭐ **RECOMENDADO**

**Propósito:** Chat interativo rodando no E2B

```bash
python chat_minimax_in_sandbox.py
```

**Experiência:**
```
💬 CHAT COM CLAUDE/MINIMAX (rodando no E2B Sandbox)
============================================================

🤖 Claude: Olá! Como posso ajudar você hoje?

💡 Digite 'sair' para encerrar o chat
============================================================

👤 Você: Explique o que é um Data Lake

🤖 Claude: Um Data Lake é um repositório centralizado...
```

**Características:**
- ✅ Chat em tempo real
- ✅ 100% isolado no E2B
- ✅ Usa Minimax API
- ✅ Interface interativa
- ✅ Digite 'sair' para encerrar

---

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar API Keys

Seu arquivo `.env` já está configurado:

```env
E2B_API_KEY=e2b_010f28305ce3797ced573788447bb9ca68707377
```

### 3. Escolher Script

```bash
# Teste básico (sem IA)
python hello_world.py

# Chat completo com Minimax ⭐
python chat_minimax_in_sandbox.py

# Teste avançado
python run_assistente_in_sandbox.py
```

---

## 🏗️ Arquitetura Detalhada

### Fluxo de uma Mensagem no Chat

```
1. Você digita: "Explique Data Lake"
   │
   ▼
2. Script local envia para E2B
   │
   ▼
3. E2B cria container isolado
   │
   ▼
4. Dentro do container:
   • Instala Anthropic SDK
   • Configura credenciais Minimax
   • Faz request para Minimax API
   │
   ▼
5. Minimax (proxy) ➜ Anthropic API
   │
   ▼
6. Resposta volta por toda cadeia
   │
   ▼
7. Você vê: "Um Data Lake é..."
   │
   ▼
8. Container E2B é destruído
```

### Comparação: Local vs E2B

| Aspecto | Rodando Local | Rodando no E2B |
|---------|---------------|----------------|
| **Isolamento** | ❌ Acessa tudo | ✅ Totalmente isolado |
| **Segurança** | ⚠️ Risco se código malicioso | ✅ Código não afeta sua máquina |
| **Persistência** | ✅ Dados ficam | ❌ Dados destruídos (proposital) |
| **Recursos** | 💻 Usa seu CPU/RAM | ☁️ Recursos dedicados na nuvem |
| **Setup** | 🔧 Instalar tudo local | 📦 Ambiente pronto |

---

## 💡 Casos de Uso

### 1. Testar Código Desconhecido
```python
# Quer testar um script que não confia?
# Execute no E2B em vez do seu computador!
```

### 2. Ambientes Limpos
```python
# Cada teste começa "zerado"
# Sem conflitos de dependências
```

### 3. Demos e Workshops
```python
# Deixe qualquer um usar seu agente
# Sem dar acesso à sua máquina
```

### 4. CI/CD
```python
# Testes de integração em ambiente isolado
# Cada pipeline = sandbox limpo
```

---

## 🎯 Próximos Passos

### Opção 1: Testar Agora
```bash
python chat_minimax_in_sandbox.py
```

### Opção 2: Customizar
Edite `chat_minimax_in_sandbox.py` e adicione:
- Histórico de conversa
- Múltiplos modelos
- Upload de arquivos
- Streaming de resposta

### Opção 3: Integrar com Projeto
Use E2B no seu `assistente-fontes`:
- Backend FastAPI roda local
- Chamadas de IA rodam no E2B
- Melhor segurança

---

## ❓ FAQ

### P: E2B é grátis?
**R:** Tem tier gratuito com limites. Veja: https://e2b.dev/pricing

### P: Posso ver o que está rodando no sandbox?
**R:** Sim! Use `sandbox.run_code("ls -la")` para explorar.

### P: E se eu quiser persistir dados?
**R:** Você pode fazer download de arquivos do sandbox antes de fechar.

### P: Posso usar com outros LLMs?
**R:** Sim! Funciona com qualquer SDK Python (OpenAI, Cohere, etc).

### P: É seguro passar minha API key?
**R:** Sim. A key só existe dentro do container isolado e é destruída ao fim.

---

## 📚 Referências

- [E2B Documentation](https://e2b.dev/docs)
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk)
- [E2B Cookbook](https://github.com/e2b-dev/e2b-cookbook)
- [Minimax API](https://api.minimax.io)

---

**Criado por:** Claude Code + E2B
**Data:** Janeiro 2026
