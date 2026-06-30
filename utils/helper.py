"""
utils/helpers.py

Common helper functions for PromptForge AI.
"""

from __future__ import annotations

from datetime import datetime
import re


def clean_prompt(text: str) -> str:
    """Normalize whitespace while preserving line breaks."""
    if not text:
        return ""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.split("\n")]
    return "\n".join(lines).strip()


def estimate_tokens(text: str) -> int:
    """
    Rough token estimate.
    Rule of thumb: ~1 token ~= 0.75 words.
    """
    words = len(text.split())
    return max(1, int(words / 0.75))


def estimate_read_time(text: str, wpm: int = 200) -> str:
    """Estimate reading time."""
    words = len(text.split())
    minutes = max(1, round(words / wpm))
    return f"{minutes} min"


def build_download_filename(prefix: str = "optimized_prompt",
                            extension: str = "txt") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def format_history_record(original: str,
                          optimized: str,
                          score: int,
                          target_model: str) -> dict:
    """Create a history record dictionary."""
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "target_model": target_model,
        "score": score,
        "original_prompt": original,
        "optimized_prompt": optimized,
    }


def readability_level(text: str) -> str:
    """Simple readability heuristic."""
    words = len(text.split())

    if words < 15:
        return "Simple"

    if words < 40:
        return "Moderate"

    return "Detailed"


def generate_statistics(original: str, optimized: str) -> dict:
    """Generate lightweight statistics for UI display."""
    return {
        "original_words": len(original.split()),
        "optimized_words": len(optimized.split()),
        "original_tokens": estimate_tokens(original),
        "optimized_tokens": estimate_tokens(optimized),
        "reading_time": estimate_read_time(optimized),
        "complexity": readability_level(optimized),
    }


if __name__ == "__main__":
    sample = "Write a Python REST API using FastAPI."
    cleaned = clean_prompt(sample)

    print(generate_statistics(sample, cleaned))
