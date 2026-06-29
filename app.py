import streamlit as st
from pathlib import Path

try:
    from models.optimizer import PromptOptimizer
except Exception:
    PromptOptimizer = None

try:
    from utils.scoring import score_prompt
except Exception:
    def score_prompt(prompt: str):
        score = 0
        suggestions = []
        if len(prompt) > 20:
            score += 20
        else:
            suggestions.append("Add more context.")
        if any(x in prompt.lower() for x in ["act as", "you are"]):
            score += 15
        else:
            suggestions.append("Specify a role/persona.")
        if "output" in prompt.lower() or "format" in prompt.lower():
            score += 15
        else:
            suggestions.append("Specify an output format.")
        if any(x in prompt.lower() for x in ["must", "only", "do not", "limit"]):
            score += 20
        else:
            suggestions.append("Add constraints.")
        if len(prompt.split()) > 25:
            score += 30
        else:
            suggestions.append("Describe the task in more detail.")
        return score, suggestions

st.set_page_config(
    page_title="PromptForge AI",
    page_icon="✨",
    layout="wide"
)

css_path = Path("assets/style.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

if "optimized" not in st.session_state:
    st.session_state.optimized = ""

st.title("✨ PromptForge AI")
st.caption("Transform simple prompts into high-quality prompts for LLMs.")

with st.sidebar:
    st.header("Settings")
    target = st.selectbox(
        "Target Model",
        ["ChatGPT", "Claude", "Gemini", "DeepSeek", "Llama", "Mistral"]
    )
    style = st.selectbox(
        "Optimization Style",
        ["Professional", "Detailed", "Concise", "Beginner", "Expert"]
    )
    temperature = st.slider("Creativity", 0.0, 1.0, 0.3)
    st.info("Phase 1: Prompt Optimization + Prompt Scoring")

left, right = st.columns([1, 1])

with left:
    prompt = st.text_area(
        "Enter your prompt",
        height=300,
        placeholder="Example: Write a resume..."
    )

    optimize = st.button("🚀 Optimize Prompt", use_container_width=True)

with right:
    st.subheader("Optimized Prompt")

    if optimize:
        if not prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Optimizing..."):
                if PromptOptimizer:
                    try:
                        model = PromptOptimizer()
                        result = model.optimize(
                            prompt=prompt,
                            target_model=target,
                            style=style,
                            temperature=temperature,
                        )
                    except Exception:
                        result = None
                else:
                    result = None

                if not result:
                    result = f"""Act as an expert.

Task:
{prompt}

Requirements:
- Be specific.
- Think step by step where appropriate.
- Produce a clear and structured answer.
- Use Markdown formatting.
- Tailor the response for {target}.
"""

                st.session_state.optimized = result

    st.text_area(
        "",
        value=st.session_state.optimized,
        height=300,
        key="optimized_box",
    )

    if st.session_state.optimized:
        st.download_button(
            "⬇ Download Prompt",
            st.session_state.optimized,
            file_name="optimized_prompt.txt",
            mime="text/plain",
            use_container_width=True,
        )

st.divider()

st.subheader("📊 Prompt Analysis")

if prompt.strip():
    score, suggestions = score_prompt(prompt)

    c1, c2 = st.columns([1, 2])

    with c1:
        st.metric("Prompt Score", f"{score}/100")
        st.progress(min(score,100) / 100)

    with c2:
        st.markdown("### Suggestions")
        if suggestions:
            for item in suggestions:
                st.write(f"• {item}")
        else:
            st.success("Excellent prompt!")

st.divider()

st.markdown(
"""
### 💡 Tips for Better Prompts

- Assign a role (e.g., *Act as a Senior ML Engineer*).
- State the goal clearly.
- Mention constraints.
- Specify the desired output format.
- Include examples when possible.
"""
)
