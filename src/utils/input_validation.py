from typing import Optional, Dict, List, Any

def validate_input(value, max_length=255, allow_empty=False):
    """Validación básica de entrada"""
    if not allow_empty and not value:
        raise ValueError("Input cannot be empty")
    if len(str(value)) > max_length:
        raise ValueError(f"Input too long. Max {max_length} characters")
    return str(value).strip()
