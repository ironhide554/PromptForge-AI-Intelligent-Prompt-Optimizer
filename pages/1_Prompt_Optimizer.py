import streamlit as st
from models.optimizer import PromptOptimizer
from models.classifier import PromptClassifier
from models.analyzer import PromptAnalyzer
from utils.prompt_stats import PromptStats
from utils.scoring import score_prompt

st.set_page_config(page_title="Prompt Optimizer",page_icon="✨",layout="wide")

@st.cache_resource
def load_optimizer():
    return PromptOptimizer()

optimizer=load_optimizer()
classifier=PromptClassifier()
analyzer=PromptAnalyzer()
stats_engine=PromptStats()

st.title("✨ Prompt Optimizer")
st.caption("Transform simple prompts into high-quality prompts for LLMs.")

target=st.sidebar.selectbox("Target Model",["ChatGPT / GPT-4o", "Claude 3.5 Sonnet", "Gemini 1.5 Pro", "DeepSeek", "Llama 3", "Mistral"])
style=st.sidebar.selectbox("Style",["Professional","Technical","Detailed","Concise","Beginner"])
temperature=st.sidebar.slider("Creativity",0.0,1.0,0.3)

if "optimized_prompt" not in st.session_state:
    st.session_state.optimized_prompt=""

# --- UI Elements ---
c1, c2 = st.columns(2)

with c1:
    prompt = st.text_area("Original Prompt", height=320, placeholder="Example: Write a resume...")
    run = st.button("🚀 Optimize", use_container_width=True)

# --- Execution Logic (MUST run before rendering the output box to prevent 1-click delay) ---
if run and prompt.strip():
    with st.spinner("Forging Prompt..."):
        try:
            result = optimizer.optimize(prompt, target_model=target, style=style, temperature=temperature)
            st.session_state.optimized_prompt = result
        except Exception as e:
            st.error(f"Error optimizing prompt: {e}")

# --- Output UI ---
with c2:
    st.text_area("Optimized Prompt", value=st.session_state.optimized_prompt, height=320)
    if st.session_state.optimized_prompt:
        st.download_button("Download", st.session_state.optimized_prompt, file_name="optimized_prompt.txt", use_container_width=True)

st.divider()

if prompt.strip():
    st.subheader("📊 Prompt Analysis")
    score, suggestions = score_prompt(prompt)
    cls = classifier.classify(prompt)
    ana = analyzer.analyze(prompt)
    stats = stats_engine.calculate(prompt)
    
    a, b, c, d = st.columns(4)
    a.metric("Score", f"{score}/100")
    b.metric("Category", cls.category)
    c.metric("Confidence", f"{int(cls.confidence*100)}%")
    d.metric("Words", stats.word_count)
    
    st.progress(score/100)
    
    st.subheader("💡 Suggestions")
    if ana.suggestions:
        for s in ana.suggestions:
            st.info(s)
    else:
        st.success("Great prompt! No suggestions.")
