import streamlit as st
from utils.helper import load_custom_css, render_sidebar_branding, render_page_header, render_footer

st.set_page_config(page_title="CoT Builder | PromptForge AI", page_icon="🧠", layout="wide")

load_custom_css()
render_sidebar_branding()

render_page_header(
    title="Chain-of-Thought (CoT) Studio",
    subtitle="Enforce step-by-step cognitive reasoning pipelines to drastically boost accuracy on complex logic, coding, and mathematical tasks.",
    icon="🧠",
    badge="REASONING PIPELINE"
)

if "cot_steps" not in st.session_state:
    st.session_state.cot_steps = [""]

st.markdown("### 1. Complex Problem Definition")
task = st.text_area(
    "What is the complex task or problem to be solved?",
    placeholder="e.g. Calculate the total cost of ownership for a 3-year Kubernetes cluster migration versus serverless Lambda architecture under 50M requests/mo...",
    height=100
)

st.markdown("### 2. Sequential Thought Steps")
st.write("Specify the logical progression the model must traverse before delivering its final answer.")

for i, step in enumerate(st.session_state.cot_steps):
    col1, col2 = st.columns([12, 1])
    with col1:
        st.session_state.cot_steps[i] = st.text_input(
            f"Step {i+1}",
            value=step,
            key=f"step_{i}",
            placeholder=f"e.g. Step {i+1}: Identify all fixed and variable cost parameters..."
        )
    with col2:
        st.write("")
        st.write("")
        if st.button("❌", key=f"del_step_{i}"):
            st.session_state.cot_steps.pop(i)
            st.rerun()

if st.button("➕ Add Reasoning Step"):
    st.session_state.cot_steps.append("")
    st.rerun()

st.divider()

st.markdown("### 3. Generated CoT Prompt Preview")

def build_cot_prompt(task_def, steps):
    prompt_parts = [task_def.strip()]
    if any(steps):
        prompt_parts.append("\nPlease think step-by-step and follow this reasoning process:")
        for i, s in enumerate(steps):
            if s.strip():
                prompt_parts.append(f"Step {i+1}: {s.strip()}")
    else:
        prompt_parts.append("\nPlease think step-by-step before answering.")
        
    return "\n".join(prompt_parts)

generated_prompt = build_cot_prompt(task, st.session_state.cot_steps)

st.code(generated_prompt, language="markdown")

from utils.api_client import generate_response, get_gemini_api_key

c1, c2, c3 = st.columns(3)
with c1:
    st.download_button("⬇ Download TXT", generated_prompt, file_name="cot_prompt.txt", mime="text/plain", use_container_width=True)
with c2:
    if st.button("🚀 Send to Optimizer", use_container_width=True):
        st.session_state.analyzer_to_optimizer_prompt = generated_prompt
        st.switch_page("pages/1_Prompt_Optimizer.py")
with c3:
    test_cot = st.button("🧪 Test with Gemini 3 Flash", use_container_width=True, type="primary")

if test_cot and generated_prompt.strip():
    api_key = get_gemini_api_key()
    if not api_key:
        st.error("Please configure your Gemini API Key in the Optimizer or Secrets to run tests.")
    else:
        with st.spinner("Executing chain-of-thought prompt on Gemini 3 Flash Preview..."):
            res = generate_response(api_key, generated_prompt)
            st.markdown("#### 🤖 Reasoning Output from `gemini-3-flash-preview`")
            if res.startswith("Error"):
                st.error(res)
            else:
                with st.chat_message("assistant"):
                    st.markdown(res)

render_footer()
