import streamlit as st
import json
from utils.helper import load_custom_css, render_sidebar_branding, render_page_header, render_footer

st.set_page_config(page_title="Few-Shot Builder | PromptForge AI", page_icon="📝", layout="wide")

load_custom_css()
render_sidebar_branding()

render_page_header(
    title="Few-Shot Prompt Studio",
    subtitle="Enforce deterministic and schema-compliant LLM outputs by providing few-shot exemplar pairs.",
    icon="📝",
    badge="IN-CONTEXT LEARNING"
)

# Session state to store examples
if "few_shot_examples" not in st.session_state:
    st.session_state.few_shot_examples = [{"input": "", "output": ""}]

st.markdown("### 1. Base Task Instruction")
base_instruction = st.text_area(
    "What should the AI do?",
    placeholder="e.g. Classify the customer feedback sentiment as Positive, Neutral, or Urgent Bug. Output only the category and confidence.",
    height=100
)

st.markdown("### 2. Exemplar Pairs")
for i, example in enumerate(st.session_state.few_shot_examples):
    st.markdown(f"**Exemplar {i+1}**")
    col1, col2, col3 = st.columns([10, 10, 1])
    with col1:
        example["input"] = st.text_input(f"Input {i+1}", value=example["input"], key=f"in_{i}", placeholder="Sample input...")
    with col2:
        example["output"] = st.text_input(f"Expected Output {i+1}", value=example["output"], key=f"out_{i}", placeholder="Expected LLM output...")
    with col3:
        st.write("")
        st.write("")
        if st.button("❌", key=f"del_{i}"):
            st.session_state.few_shot_examples.pop(i)
            st.rerun()

if st.button("➕ Add Another Exemplar"):
    st.session_state.few_shot_examples.append({"input": "", "output": ""})
    st.rerun()

st.divider()

st.markdown("### 3. Generated Prompt Preview")

def build_few_shot_prompt(instruction, examples):
    prompt_parts = [instruction.strip()]
    if examples:
        prompt_parts.append("\nHere are reference examples:")
        for ex in examples:
            if ex["input"] or ex["output"]:
                prompt_parts.append(f"Input: {ex['input']}\nOutput: {ex['output']}\n")
    prompt_parts.append("Input: [YOUR INPUT HERE]\nOutput: ")
    return "\n".join(prompt_parts)

generated_prompt = build_few_shot_prompt(base_instruction, st.session_state.few_shot_examples)

st.code(generated_prompt, language="markdown")

from utils.api_client import generate_response, get_gemini_api_key

c1, c2, c3 = st.columns(3)
with c1:
    st.download_button("⬇ Download TXT", generated_prompt, file_name="few_shot_prompt.txt", mime="text/plain", use_container_width=True)
with c2:
    if st.button("🚀 Send to Optimizer", use_container_width=True):
        st.session_state.analyzer_to_optimizer_prompt = generated_prompt
        st.switch_page("pages/1_Prompt_Optimizer.py")
with c3:
    test_few_shot = st.button("🧪 Test with Gemini 3 Flash", use_container_width=True, type="primary")

if test_few_shot and generated_prompt.strip():
    api_key = get_gemini_api_key()
    if not api_key:
        st.error("Please configure your Gemini API Key in the Optimizer or Secrets to run tests.")
    else:
        with st.spinner("Executing prompt on Gemini 3 Flash Preview..."):
            test_prompt = generated_prompt.replace("[YOUR INPUT HERE]", "Analyze standard test sample")
            res = generate_response(api_key, test_prompt)
            st.markdown("#### 🤖 Output from `gemini-3-flash-preview`")
            if res.startswith("Error"):
                st.error(res)
            else:
                with st.chat_message("assistant"):
                    st.markdown(res)

render_footer()
