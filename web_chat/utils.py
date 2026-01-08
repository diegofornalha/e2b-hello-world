"""
Funções utilitárias compartilhadas

Helpers para escape de strings, truncamento de logs e outras utilidades.
"""

def escape_for_python_code(text: str) -> str:
    """
    Escapa string para injetar com segurança em código Python

    Args:
        text: Texto a ser escapado

    Returns:
        Texto escapado seguro para usar em f-strings

    Examples:
        >>> escape_for_python_code("Hello 'world'")
        "Hello \\'world\\'"
    """
    return text.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')

def truncate_log(text: str, max_len: int = 100) -> str:
    """
    Trunca texto para logs mantendo legibilidade

    Args:
        text: Texto a truncar
        max_len: Tamanho máximo (padrão 100)

    Returns:
        Texto truncado com "..." se necessário

    Examples:
        >>> truncate_log("A" * 150, 100)
        "AAAA...AAA"
    """
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."
