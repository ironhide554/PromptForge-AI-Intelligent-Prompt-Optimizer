import json
from pathlib import Path

from utils.helper import load_custom_css, render_sidebar_branding, render_page_header, render_footer

st.set_page_config(
    page_title="Prompt History | PromptForge AI",
    page_icon="🕒",
    layout="wide"
)

load_custom_css()
render_sidebar_branding()

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

render_page_header(
    title="Prompt History & Audit Trail",
    subtitle="Review previous optimizations, track quality trends over time, or re-export prompt artifacts.",
    icon="🕒",
    badge="AUDIT LOG"
)

history = load_history()

if not history:
    st.info("No prompt history available yet. Generate an optimized prompt in the Optimizer to build your audit log.")
    render_footer()
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

search_mode = st.sidebar.radio("Search Mode", ["Keyword", "Semantic (AI)"], help="Semantic search uses embeddings to find prompts by meaning.")

search = st.text_input(
    "🔍 Search Prompt",
    placeholder="Search by keyword or concept..."
)

# Pre-filter by category and target model
pre_filtered = []
for item in history:
    cat_match = (selected_category == "All") or (item.get("category", "General") == selected_category)
    tgt_match = (selected_target == "All") or (item.get("target_model", "ChatGPT") == selected_target)
    if cat_match and tgt_match:
        pre_filtered.append(item)

filtered = []
if search and search_mode == "Semantic (AI)":
    from utils.embeddings import semantic_search
    texts_to_search = [item.get("optimized_prompt", "") + " " + item.get("original_prompt", "") for item in pre_filtered]
    with st.spinner("Searching semantically..."):
        indices = semantic_search(search, texts_to_search, top_k=10)
    filtered = [pre_filtered[i] for i in indices]
else:
    for item in pre_filtered:
        text = (
            item.get("original_prompt", "") +
            item.get("optimized_prompt", "") +
            item.get("category", "")
        ).lower()
        search_match = (search.lower() in text) if search else True
        if search_match:
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

        cols = st.columns(4)
        cols[0].markdown(f"**Category:** {item.get('category','General')}")
        cols[1].markdown(f"**Score:** {item.get('score','-')}/100")
        cols[2].markdown(f"**Target Model:** {item.get('target_model','ChatGPT')}")
        cols[3].markdown(f"**Style:** {item.get('style','Professional')}")

        st.caption(f"🕒 *Optimized on: {item.get('timestamp','Unknown')}*")

        st.markdown("### 📝 Original Prompt")

        st.info(
            item.get("original_prompt","")
        )

        st.markdown("### ✨ Optimized Prompt")

        st.code(
            item.get("optimized_prompt",""),
            language="markdown"
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.download_button(
                "📄 Download TXT",
                item.get("optimized_prompt",""),
                file_name=f"prompt_{index+1}.txt",
                mime="text/plain",
                key=f"download_{index}"
            )

        with c2:
            try:
                from utils.pdf_generator import generate_pdf
                pdf_bytes = generate_pdf(item.get("optimized_prompt",""))
                st.download_button(
                    "📑 Download PDF",
                    pdf_bytes,
                    file_name=f"prompt_{index+1}.pdf",
                    mime="application/pdf",
                    key=f"pdf_dl_{index}"
                )
            except Exception:
                st.error("PDF Error")

        with c3:
            if st.button(
                "❌ Delete",
                key=f"delete_{index}"
            ):

                history.remove(item)

                save_history(history)

                st.rerun()

render_footer()