import json
from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Prompt History",
    page_icon="🕒",
    layout="wide"
)

# -------------------------------------
# Configuration
# -------------------------------------

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

HISTORY_FILE = DATA_DIR / "history.json"


# -------------------------------------
# Helper Functions
# -------------------------------------

def load_history():

    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return []


def save_history(history):

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)


# -------------------------------------
# UI
# -------------------------------------

st.title("🕒 Prompt History")

history = load_history()

if not history:

    st.info("No prompt history available.")

    st.stop()

# -------------------------------------
# Search
# -------------------------------------

search = st.text_input(
    "🔍 Search Prompt",
    placeholder="Search by prompt or category..."
)

filtered = []

for item in history:

    text = (
        item.get("original_prompt", "") +
        item.get("category", "")
    ).lower()

    if search.lower() in text:
        filtered.append(item)

# -------------------------------------
# Buttons
# -------------------------------------

col1, col2 = st.columns([1, 1])

with col1:

    if st.button("🗑 Clear History"):

        save_history([])

        st.success("History Cleared")

        st.rerun()

with col2:

    st.metric(
        "Total Prompts",
        len(filtered)
    )

st.divider()

# -------------------------------------
# Display History
# -------------------------------------

for index, item in enumerate(reversed(filtered)):

    with st.expander(
        f"📄 Prompt {len(filtered)-index}"
    ):

        st.markdown(
            f"**Category:** {item.get('category','General')}"
        )

        st.markdown(
            f"**Score:** {item.get('score','-')}/100"
        )

        st.markdown(
            f"**Target Model:** {item.get('target_model','ChatGPT')}"
        )

        st.markdown(
            f"**Date:** {item.get('timestamp','Unknown')}"
        )

        st.markdown("### Original Prompt")

        st.code(
            item.get("original_prompt",""),
            language="text"
        )

        st.markdown("### Optimized Prompt")

        st.code(
            item.get("optimized_prompt",""),
            language="text"
        )

        c1, c2 = st.columns(2)

        with c1:

            st.download_button(
                "⬇ Download",
                item.get("optimized_prompt",""),
                file_name=f"prompt_{index+1}.txt",
                mime="text/plain",
                key=f"download_{index}"
            )

        with c2:

            if st.button(
                "❌ Delete",
                key=f"delete_{index}"
            ):

                history.remove(item)

                save_history(history)

                st.rerun()

st.divider()

st.caption("PromptForge AI • Prompt History")