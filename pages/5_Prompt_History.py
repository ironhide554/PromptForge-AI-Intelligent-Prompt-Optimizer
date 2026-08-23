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

st.sidebar.header("Filter History")
categories = ["All"] + sorted(list(set([item.get("category", "General") for item in history])))
selected_category = st.sidebar.selectbox("Category", categories)

targets = ["All"] + sorted(list(set([item.get("target_model", "ChatGPT") for item in history])))
selected_target = st.sidebar.selectbox("Target Model", targets)

sort_by = st.sidebar.radio("Sort By", ["Newest First", "Oldest First", "Highest Score"])

search = st.text_input(
    "🔍 Search Prompt",
    placeholder="Search by keyword..."
)

filtered = []
for item in history:
    cat_match = (selected_category == "All") or (item.get("category", "General") == selected_category)
    tgt_match = (selected_target == "All") or (item.get("target_model", "ChatGPT") == selected_target)
    
    text = (
        item.get("original_prompt", "") +
        item.get("optimized_prompt", "") +
        item.get("category", "")
    ).lower()
    search_match = (search.lower() in text)

    if cat_match and tgt_match and search_match:
        filtered.append(item)

if sort_by == "Newest First":
    filtered = list(reversed(filtered))
elif sort_by == "Oldest First":
    pass # original order is oldest first
elif sort_by == "Highest Score":
    filtered.sort(key=lambda x: x.get("score", 0), reverse=True)

# -------------------------------------
# Analytics
# -------------------------------------
if filtered:
    st.subheader("📈 History Analytics")
    avg_score = sum([i.get("score", 0) for i in filtered]) / len(filtered)
    
    targets_list = [i.get("target_model", "ChatGPT") for i in filtered]
    most_freq_target = max(set(targets_list), key=targets_list.count)
    
    cat_list = [i.get("category", "General") for i in filtered]
    most_freq_cat = max(set(cat_list), key=cat_list.count)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Prompts", len(filtered))
    m2.metric("Average Score", f"{int(avg_score)}/100")
    m3.metric("Top Target Model", most_freq_target)
    m4.metric("Top Category", most_freq_cat)
    
    st.divider()

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
    pass

st.divider()

# -------------------------------------
# Display History
# -------------------------------------

for index, item in enumerate(filtered):

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