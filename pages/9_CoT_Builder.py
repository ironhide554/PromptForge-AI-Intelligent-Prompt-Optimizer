import streamlit as st

st.set_page_config(page_title="CoT Builder", page_icon="🧠", layout="wide")

st.title("🧠 Chain-of-Thought Builder")
st.caption("Force the AI to think step-by-step to improve reasoning and accuracy.")

if "cot_steps" not in st.session_state:
    st.session_state.cot_steps = [""]

st.markdown("### 1. Task Definition")
task = st.text_area(
    "What is the complex problem?",
    placeholder="e.g. Solve this math problem: 2x + 5 = 15",
    height=100
)

st.markdown("### 2. Reasoning Steps")
st.write("Define the sequence of thoughts the AI should follow.")

for i, step in enumerate(st.session_state.cot_steps):
    col1, col2 = st.columns([12, 1])
    with col1:
        st.session_state.cot_steps[i] = st.text_input(f"Step {i+1}", value=step, key=f"step_{i}", placeholder="e.g. First, analyze the problem...")
    with col2:
        st.write("")
        st.write("")
        if st.button("❌", key=f"del_step_{i}"):
            st.session_state.cot_steps.pop(i)
            st.rerun()

if st.button("➕ Add Step"):
    st.session_state.cot_steps.append("")
    st.rerun()

st.divider()

st.markdown("### 3. Generate & Preview")

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

st.code(generated_prompt, language="text")

c1, c2, c3 = st.columns(3)
with c1:
    st.download_button("⬇ Download TXT", generated_prompt, file_name="cot_prompt.txt", mime="text/plain")
with c2:
    if st.button("🚀 Send to Optimizer"):
        st.session_state.analyzer_to_optimizer_prompt = generated_prompt
        st.switch_page("pages/1_Prompt_Optimizer.py")
