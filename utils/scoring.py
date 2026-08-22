import re
from typing import List, Tuple

ROLE_PATTERNS = [
    "act as", "you are", "behave as", "assume the role", "role:", "imagine you are"
]

FORMAT_PATTERNS = [
    "markdown", "json", "table", "bullet", "csv", "xml",
    "output", "format", "response format", "structure"
]

CONSTRAINT_PATTERNS = [
    "must", "only", "do not", "don't", "without",
    "maximum", "minimum", "limit", "exactly", "under", "at least", "ensure"
]

EXAMPLE_PATTERNS = [
    "example", "for example", "sample", "such as", "like this:"
]


def _contains_any(text: str, patterns: List[str]) -> bool:
    t = text.lower()
    return any(p in t for p in patterns)


def score_prompt(prompt: str) -> Tuple[int, List[str]]:
    """
    Evaluates a prompt and provides a quality score and suggestions.
    
    Args:
        prompt (str): The user's prompt.
        
    Returns:
        Tuple[int, List[str]]: score (0-100) and list of suggestions.
    """
    text = prompt.strip()
    lower = text.lower()

    score = 0
    suggestions = []

    # Length (15)
    wc = len(text.split())
    if wc >= 40:
        score += 15
    elif wc >= 20:
        score += 10
    elif wc >= 10:
        score += 5
    else:
        suggestions.append("Add more context and describe the task in greater detail.")

    # Role / Persona (15)
    if _contains_any(lower, ROLE_PATTERNS):
        score += 15
    else:
        suggestions.append("Assign a role/persona (e.g. 'Act as a senior data scientist').")

    # Goal clarity (15)
    if len(re.findall(r"\b(create|write|generate|build|explain|analyze|summarize|design)\b", lower)) > 0:
        score += 15
    else:
        suggestions.append("Clearly state the objective using an action verb.")

    # Constraints (15)
    if _contains_any(lower, CONSTRAINT_PATTERNS):
        score += 15
    else:
        suggestions.append("Add constraints such as length, tone, or things to avoid.")

    # Output format (15)
    if _contains_any(lower, FORMAT_PATTERNS):
        score += 15
    else:
        suggestions.append("Specify the desired output format (Markdown, JSON, table, etc.).")

    # Context (15)
    if wc >= 25:
        score += 15
    else:
        suggestions.append("Provide background information or relevant context.")

    # Examples (10)
    if _contains_any(lower, EXAMPLE_PATTERNS):
        score += 10
    else:
        suggestions.append("Include an example to guide the AI, if applicable.")

    # Specificity (extra 0-5)
    if any(ch.isdigit() for ch in text) or '"' in text or "'" in text:
        score += 5

    score = min(score, 100)

    if score >= 90:
        level = "Excellent"
    elif score >= 75:
        level = "Good"
    elif score >= 50:
        level = "Average"
    else:
        level = "Needs Improvement"

    return score, suggestions


if __name__ == "__main__":
    sample = """Act as a senior Python developer.
Create a REST API using FastAPI.
Output the answer in Markdown.
Do not use external databases.
Include an example."""
    s, tips = score_prompt(sample)
    print("Score:", s)
    print("Suggestions:", tips)
