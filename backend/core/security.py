import re


def sanitize_input(text: str) -> str:
    """
    Remove potential prompt injection patterns from user input.
    """
    dangerous_patterns = [
        "ignore previous",
        "ignore all",
        "forget everything",
        "new instructions",
        "system:",
        "</system>",
        "you are now",
        "act as",
        "pretend to be",
        "--- CONTEXT DATA ---",
        "--- END CONTEXT DATA ---",
        "</student_input>",
        "<student_input>",
        "ignore the",
        "disregard",
    ]

    # Remove dangerous patterns (case-insensitive)
    for pattern in dangerous_patterns:
        text = re.sub(re.escape(pattern), "", text, flags=re.IGNORECASE)
    # Remove template injection attempts (curly braces)
    text = text.replace("{", "").replace("}", "")

    return text.strip()
