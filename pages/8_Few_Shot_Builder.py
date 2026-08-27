import streamlit as st
import json

st.set_page_config(page_title="Few-Shot Builder", page_icon="📝", layout="wide")

st.title("📝 Few-Shot Prompt Builder")
st.caption("Construct powerful prompts by providing examples (few-shot learning).")

# Session state to store examples
if "few_shot_examples" not in st.session_state:
    st.session_state.few_shot_examples = [{"input": "", "output": ""}]

st.markdown("### 1. Base Instruction")
base_instruction = st.text_area(
    "What should the AI do?",
    placeholder="e.g. Classify the sentiment of the given text as Positive, Negative, or Neutral.",
    height=100
)

st.markdown("### 2. Examples")
for i, example in enumerate(st.session_state.few_shot_examples):
    st.markdown(f"**Example {i+1}**")
    col1, col2, col3 = st.columns([10, 10, 1])
    with col1:
        example["input"] = st.text_input(f"Input {i+1}", value=example["input"], key=f"in_{i}")
    with col2:
        example["output"] = st.text_input(f"Output {i+1}", value=example["output"], key=f"out_{i}")
    with col3:
        st.write("")
        st.write("")
        if st.button("❌", key=f"del_{i}"):
            st.session_state.few_shot_examples.pop(i)
            st.rerun()

if st.button("➕ Add Example"):
    st.session_state.few_shot_examples.append({"input": "", "output": ""})
    st.rerun()

st.divider()

st.markdown("### 3. Generate & Preview")

def build_few_shot_prompt(instruction, examples):
    prompt_parts = [instruction.strip()]
    if examples:
        prompt_parts.append("\nHere are some examples:")
        for ex in examples:
            if ex["input"] or ex["output"]:
                prompt_parts.append(f"Input: {ex['input']}\nOutput: {ex['output']}\n")
    prompt_parts.append("Input: [YOUR INPUT HERE]\nOutput: ")
    return "\n".join(prompt_parts)

generated_prompt = build_few_shot_prompt(base_instruction, st.session_state.few_shot_examples)

st.code(generated_prompt, language="text")

c1, c2, c3 = st.columns(3)
with c1:
    st.download_button("⬇ Download TXT", generated_prompt, file_name="few_shot_prompt.txt", mime="text/plain")
with c2:
    if st.button("🚀 Send to Optimizer"):
        st.session_state.analyzer_to_optimizer_prompt = generated_prompt
        st.switch_page("pages/1_Prompt_Optimizer.py")
