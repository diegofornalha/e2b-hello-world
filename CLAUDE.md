# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python project demonstrating secure, isolated code execution using E2B Cloud Sandbox with Claude/Minimax LLM integration.

**Stack**: Python 3 + FastAPI + E2B Code Interpreter + Anthropic SDK (via Minimax proxy)

## Architecture Pattern

```
Local Machine → E2B API → Cloud Sandbox (isolated) → Claude/Minimax API
```

All code execution happens in isolated E2B cloud sandboxes - no local system access from executed code.

## Essential Commands

```bash
# Setup
cp .env.example .env  # Add E2B_API_KEY
pip install -r requirements.txt

# Run web server (port 8000)
python server_simples.py

# Test basic sandbox
python hello_world.py

# Interactive chat
python chat_minimax_in_sandbox.py

# Run tests
python tests/test_api.py
python tests/test_minimax_simple.py
python tests/test_final.py
```

## Key Entry Points

| Script | Purpose |
|--------|---------|
| `hello_world.py` | Basic E2B sandbox test |
| `server_simples.py` | FastAPI web server (port 8000) |
| `chat_minimax_in_sandbox.py` | Interactive terminal chat |
| `agent_in_sandbox.py` | Claude Agent SDK in sandbox |
| `run_assistente_in_sandbox.py` | External project execution |

## API Endpoints (server_simples.py)

- `GET /` - Web interface
- `POST /chat` - Chat endpoint
- `GET /health` - Health check

## Configuration

Required in `.env`:
```
E2B_API_KEY=e2b_***      # Get from https://e2b.dev/dashboard?tab=keys
MINIMAX_TOKEN=sk-cp-***  # Get from https://www.minimax.io/
```

## LLM Integration

- **Provider**: Minimax as Anthropic API proxy
- **Base URL**: `https://api.minimax.io/anthropic`
- **Model**: `minimax/minimax-m2`

## Debug Tools

- `explore_sandbox.py` - Explore E2B filesystem
- `check_e2b_output.py` - Debug sandbox outputs
- `debug_minimax.py` / `debug_minimax2.py` - Minimax API debugging
