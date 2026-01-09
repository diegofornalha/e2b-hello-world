def escape_for_python_code(text: str) -> str:

    return text.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')

def truncate_log(text: str, max_len: int = 100) -> str:
    if len(text) <= max_len:
        return text
    return text[:max_len] + "..."
