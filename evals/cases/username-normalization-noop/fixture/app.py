def normalize_username(value: str) -> str:
    """Canonicalize a username before lookup and uniqueness checks."""
    return value.strip().lower()
