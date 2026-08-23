import streamlit as st
from models.classifier import PromptClassifier
from models.analyzer import PromptAnalyzer
from utils.prompt_stats import PromptStats
from utils.scoring import score_prompt
from utils.api_client import generate_response

st.set_page_config(page_title="Prompt Optimizer",page_icon="✨",layout="wide")
classifier=PromptClassifier()
analyzer=PromptAnalyzer()
stats_engine=PromptStats()

st.title("✨ Prompt Optimizer")
st.caption("Transform simple prompts into high-quality prompts for LLMs.")

provider = st.sidebar.selectbox("AI Provider", ["OpenAI", "Anthropic", "Google Gemini"])
api_key = st.sidebar.text_input(f"{provider} API Key", type="password", help="Required for Cloud AI optimization")
if provider == "OpenAI":
    opt_model = "gpt-4o-mini"
elif provider == "Anthropic":
    opt_model = "claude-3-haiku-20240307"
else:
    if api_key:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        try:
            available_models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            available_models.sort(reverse=True) # Put newer versions higher up
            
            default_idx = 0
            for i, m in enumerate(available_models):
                if "3.6-flash" in m:
                    default_idx = i
                    break
            
            opt_model = st.sidebar.selectbox("Select Gemini Model", available_models, index=default_idx)
        except Exception:
            opt_model = "gemini-3.6-flash"
    else:
        opt_model = "gemini-3.6-flash"
        
st.sidebar.markdown("---")
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

# --- Execution Logic ---
if run and prompt.strip():
    with st.spinner("Forging Prompt..."):
        try:
            if not api_key:
                st.error("Please enter your API Key in the sidebar to use the Optimizer.")
                result = ""
            else:
                meta_prompt = f"""You are an expert Prompt Engineer. Rewrite the following user prompt into a highly structured, professional prompt.
Requirements:
- Optimize it for: {target}
- Desired Style: {style}
- Give the AI a specific persona/role.
- Clarify the task and add constraints.
- Output ONLY the newly optimized prompt. Do not include any conversational filler.

User's Original Prompt:
{prompt}
"""
                result = generate_response(provider, api_key, meta_prompt, opt_model)
        
            if result and not result.startswith("Error"):
                st.session_state.optimized_prompt = result
                from utils.history_manager import add_to_history
                from models.classifier import PromptClassifier
                from utils.scoring import score_prompt
                # Calculate category and score for the optimized prompt
                c = PromptClassifier().classify(result)
                s, _ = score_prompt(result)
                add_to_history(prompt, result, c.category, s, target, style)
            elif result.startswith("Error"):
                st.error(result)
        except Exception as e:
            st.error(f"Error optimizing prompt: {e}")

# --- Output UI ---
with c2:
    st.text_area("Optimized Prompt", value=st.session_state.optimized_prompt, height=320)
    if st.session_state.optimized_prompt:
        st.download_button("Download", st.session_state.optimized_prompt, file_name="optimized_prompt.txt", use_container_width=True)

st.divider()

if prompt.strip():
    if not st.session_state.optimized_prompt:
        # Just show original if no optimization has run yet
        st.subheader("📊 Original Prompt Analysis")
        score, _ = score_prompt(prompt)
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
    else:
        st.subheader("📊 Optimization Results")
        
        # Original
        o_score, _ = score_prompt(prompt)
        o_cls = classifier.classify(prompt)
        o_stats = stats_engine.calculate(prompt)
        
        # Optimized
        opt_score, _ = score_prompt(st.session_state.optimized_prompt)
        opt_cls = classifier.classify(st.session_state.optimized_prompt)
        opt_ana = analyzer.analyze(st.session_state.optimized_prompt)
        opt_stats = stats_engine.calculate(st.session_state.optimized_prompt)
        
        col_orig, col_opt = st.columns(2)
        with col_orig:
            st.markdown("### 📝 Original")
            st.metric("Score", f"{o_score}/100")
            st.caption(f"Words: **{o_stats.word_count}** | Category: **{o_cls.category}**")
            
        with col_opt:
            st.markdown("### ✨ Optimized")
            st.metric("Score", f"{opt_score}/100", delta=f"{opt_score - o_score} points")
            st.caption(f"Words: **{opt_stats.word_count}** | Category: **{opt_cls.category}**")
            
        st.progress(opt_score/100, text=f"Optimized Prompt Quality: {opt_score}%")
        
        st.subheader("💡 Final Suggestions")
        if opt_ana.suggestions:
            for s in opt_ana.suggestions:
                st.info(s)
        else:
            st.success("This prompt is fully optimized and ready to use! ✨")
