#!/usr/bin/env python3
"""
Verificar formato de output do E2B
"""
from e2b_code_interpreter import Sandbox
from dotenv import load_dotenv

load_dotenv()

print("🔍 Verificando formato de output do E2B\n")

with Sandbox.create() as s:
    result = s.run_code('print("Hello World!")')

    print("📊 Atributos disponíveis:")
    attrs = [x for x in dir(result) if not x.startswith('_')]
    for attr in attrs:
        val = getattr(result, attr)
        if not callable(val):
            print(f"   • {attr}: {type(val).__name__} = {repr(val)[:100]}")

    print("\n📝 Testando diferentes tipos de output:")

    # Teste 1: Print
    r1 = s.run_code('print("Test 1")')
    print(f"\n1. Print:")
    print(f"   text: {r1.text}")
    print(f"   error: {r1.error}")

    # Teste 2: Expression value
    r2 = s.run_code('2 + 2')
    print(f"\n2. Expression:")
    print(f"   text: {r2.text}")
    print(f"   error: {r2.error}")

    # Teste 3: Variable and print
    r3 = s.run_code('x = "hello"; print(x)')
    print(f"\n3. Variable + print:")
    print(f"   text: {r3.text}")
    print(f"   error: {r3.error}")
