import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="PromptForge AI | Home",
    page_icon="✨",
    layout="wide"
)

css_path = Path("assets/style.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

st.title("✨ Welcome to PromptForge AI")
st.markdown("### The Intelligent Prompt Optimizer using Cloud AI Models")

st.divider()

st.markdown("""
Welcome to **PromptForge AI**! This tool is designed to help you transform simple, vague prompts into highly structured, professional prompts tailored for modern Large Language Models (LLMs) like ChatGPT, Claude, and Gemini.

### 🧭 Navigation
Please use the sidebar on the left to navigate through the tools, or click the quick links below:
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 🚀 Prompt Optimizer")
    st.write("Convert basic prompts into professional, highly-structured prompts using state-of-the-art Cloud AI models.")
    st.page_link("pages/1_Prompt_Optimizer.py", label="Go to Optimizer", icon="🚀")

with col2:
    st.info("### 📊 Prompt Analyzer")
    st.write("Analyze the quality, readability, and statistics of your prompts. Get actionable improvement suggestions.")
    st.page_link("pages/2_Prompt_Analyzer.py", label="Go to Analyzer", icon="📊")
    
with col3:
    st.info("### 🧪 Live Sandbox")
    st.write("Test your optimized prompts directly against live LLMs securely using your own API keys.")
    st.page_link("pages/7_Sandbox.py", label="Go to Sandbox", icon="🧪")

st.write("")
st.write("")

c1, c2, c3 = st.columns(3)

with c1:
    st.info("### 📝 Few-Shot Builder")
    st.write("Construct powerful prompts by easily providing input/output examples.")
    st.page_link("pages/8_Few_Shot_Builder.py", label="Go to Few-Shot", icon="📝")

with c2:
    st.info("### 🧠 CoT Builder")
    st.write("Force AI to think step-by-step to improve reasoning and accuracy.")
    st.page_link("pages/9_CoT_Builder.py", label="Go to CoT Builder", icon="🧠")

with c3:
    st.info("### 🌐 Marketplace")
    st.write("Discover and download prompt templates shared by the community.")
    st.page_link("pages/4_Prompt_Library.py", label="Go to Marketplace", icon="🌐")

st.divider()

st.markdown("""
### 💡 Why use PromptForge?
- **Better Outputs:** LLMs perform significantly better when given specific roles, constraints, and output formats.
- **Save Time:** Stop writing long prompts manually. Give us the core idea, and we forge the rest.
- **Cost Effective:** Well-structured prompts reduce the need for back-and-forth prompting, saving you API tokens.
""")
