# E2B Hello World com Claude Agent SDK

Este projeto demonstra como executar o Claude Agent SDK dentro de um sandbox E2B isolado e seguro.

## Estrutura

```
📦 e2b-hello-world/
├── 📄 requirements.txt          # Dependências Python
├── 📄 .env.example              # Exemplo de variáveis de ambiente
├── 📄 hello_world.py            # Teste básico do E2B
├── 📄 agent_in_sandbox.py       # Claude Agent SDK rodando no E2B
└── 📄 README.md                 # Este arquivo
```

## O que é E2B?

**E2B** é um provedor de sandboxes isolados na nuvem. Ele permite executar código de forma segura, sem expor seu sistema local a riscos.

## Por que usar E2B com Claude Agent SDK?

1. **Segurança**: Agentes executam código em ambiente isolado
2. **Isolamento de Segredos**: Seus dados de produção ficam protegidos
3. **Escalabilidade**: Sandboxes na nuvem podem escalar conforme necessário

## Arquitetura

```
Seu Computador Local
    │
    ▼
┌─────────────────────────────┐
│  Python Script              │
│  - Conecta ao E2B           │
│  - Envia tarefas            │
└─────────────────────────────┘
    │
    ▼ (API E2B)
┌─────────────────────────────┐
│  E2B Cloud Sandbox          │
│  ┌───────────────────────┐  │
│  │ Claude Agent SDK      │  │
│  │ - Executa tarefas     │  │
│  │ - Manipula arquivos   │  │
│  │ - Retorna resultados  │  │
│  └───────────────────────┘  │
└─────────────────────────────┘
```

## Configuração

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar API Keys

Copie o arquivo `.env.example` para `.env` e preencha com suas chaves:

```bash
cp .env.example .env
```

Edite o `.env` e adicione:
- **E2B_API_KEY**: Obtenha em https://e2b.dev/dashboard?tab=keys
- **ANTHROPIC_API_KEY**: Obtenha em https://console.anthropic.com/

### 3. Testar E2B básico

```bash
python hello_world.py
```

### 4. Executar Claude Agent SDK no sandbox

```bash
python agent_in_sandbox.py
```

## Como funciona

### hello_world.py
Teste básico que:
1. Cria um sandbox E2B
2. Executa código Python simples
3. Mostra o resultado

### agent_in_sandbox.py
Demonstração avançada que:
1. Cria um sandbox E2B
2. Instala o Claude Agent SDK dentro do sandbox
3. Executa um agente que resolve tarefas
4. Retorna os resultados com segurança

## Exemplos de Uso

```python
from e2b_code_interpreter import Sandbox

# Criar sandbox
with Sandbox.create() as sandbox:
    # Executar código Python
    result = sandbox.run_code("print('Hello from E2B!')")
    print(result.text)  # Output: Hello from E2B!
```

## Referências

- [E2B Documentation](https://e2b.dev/docs)
- [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk)
- [E2B Cookbook](https://github.com/e2b-dev/e2b-cookbook)
