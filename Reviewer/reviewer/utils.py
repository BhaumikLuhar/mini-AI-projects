def estimate_tokens(
    text: str,
) -> int:
    """
    Rough token estimate.

    1 token ≈ 4 chars
    """

    return max(
        1,
        len(text) // 4
    )