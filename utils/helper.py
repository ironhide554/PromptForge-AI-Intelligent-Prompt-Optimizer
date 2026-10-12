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


def load_custom_css():
    """Injects the enterprise style system and brand identity across pages."""
    import streamlit as st
    from pathlib import Path
    css_path = Path("assets/style.css")
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def render_sidebar_branding():
    """Renders cohesive sidebar branding."""
    import streamlit as st
    with st.sidebar:
        st.markdown("""
        <div style="padding: 0.25rem 0 0.85rem 0; border-bottom: 1px solid rgba(255,255,255,0.07); margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 4px;">
                <span style="font-size: 1.4rem;">✨</span>
                <span style="font-weight: 800; font-size: 1.15rem; background: linear-gradient(135deg, #A5B4FC, #818CF8, #38BDF8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">PromptForge AI</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #10B981; box-shadow: 0 0 6px #10B981;"></span>
                <span style="font-size: 0.75rem; color: #94A3B8; font-weight: 600;">Gemini 3 Flash Preview • Active</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str, icon: str = "✨", badge: str = "PROMPT STUDIO"):
    """Renders an executive page header banner."""
    import streamlit as st
    st.markdown(f"""
    <div style="margin-bottom: 1.75rem;">
        <div class="pf-pill">
            <span class="pf-pill-dot"></span>
            <span>{badge}</span>
        </div>
        <h1 style="margin: 0 0 0.4rem 0; font-size: 2.25rem;">
            <span>{icon}</span> <span class="pf-gradient-title">{title}</span>
        </h1>
        <p style="color: #94A3B8; font-size: 1.05rem; margin: 0; line-height: 1.5;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    """Renders the standard sleek platform footer."""
    import streamlit as st
    st.markdown("""
    <div class="pf-footer-container">
        <div style="display: flex; justify-content: center; align-items: center; gap: 16px; margin-bottom: 0.75rem; flex-wrap: wrap;">
            <span class="pf-status-badge">
                <span style="width: 6px; height: 6px; border-radius: 50%; background: #10B981; display: inline-block;"></span>
                Gemini Cloud Engine Online
            </span>
            <span style="color: #64748B;">•</span>
            <span style="color: #94A3B8; font-size: 0.825rem;">Exclusively powered by Google Gemini 3 Flash Preview (gemini-3-flash-preview)</span>
        </div>
        <p style="margin: 0; color: #64748B; font-size: 0.8rem;">PromptForge AI © 2026 • Intelligent Prompt Optimizer</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    sample = "Write a Python REST API using FastAPI."
    cleaned = clean_prompt(sample)

    print(generate_statistics(sample, cleaned))

