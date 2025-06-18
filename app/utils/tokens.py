"""Simple token estimator used to limit prompt size."""

def count_tokens(text: str) -> int:
    """Return a rough token count for ``text``.

    Uses a heuristic of 4 characters per token, which is sufficient for
    controlling prompt length without external dependencies.
    """
    return max(1, len(text) // 4)
