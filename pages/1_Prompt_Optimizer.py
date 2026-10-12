import streamlit as st
from models.classifier import PromptClassifier
from models.analyzer import PromptAnalyzer
from utils.prompt_stats import PromptStats
from utils.scoring import score_prompt
from utils.api_client import generate_response
from utils.helper import load_custom_css, render_sidebar_branding, render_page_header, render_footer

st.set_page_config(page_title="Prompt Optimizer | PromptForge AI", page_icon="✨", layout="wide")

load_custom_css()
render_sidebar_branding()

classifier = PromptClassifier()
analyzer = PromptAnalyzer()
stats_engine = PromptStats()

render_page_header(
    title="Prompt Optimizer",
    subtitle="Transform raw prompts into professional, multi-layered instructions tailored for modern LLMs.",
    icon="✨",
    badge="FORGE STUDIO"
)

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("### ⚡ Gemini Engine")
    st.markdown("""
    <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 10px; padding: 10px 12px; margin-bottom: 12px;">
        <div style="display: flex; align-items: center; gap: 6px;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #6366F1; display: inline-block;"></span>
            <span style="font-weight: 700; font-size: 0.85rem; color: #A5B4FC;">Gemini 3 Flash Preview</span>
        </div>
        <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 4px;">Exclusive Model: <code>gemini-3-flash-preview</code></div>
    </div>
    """, unsafe_allow_html=True)
    
    from utils.api_client import get_gemini_api_key, set_gemini_api_key
    cached_key = get_gemini_api_key()
    
    api_key = st.text_input(
        "Gemini API Key",
        value=cached_key,
        type="password",
        help="Required for Gemini Cloud AI optimization. Auto-resolved from Secrets, .env, or session.",
        placeholder="AIzaSy..."
    )
    if api_key:
        set_gemini_api_key(api_key)
        st.markdown("<span style='color: #34D399; font-size: 0.75rem;'>🟢 Gemini Key Ready</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span style='color: #F87171; font-size: 0.75rem;'>🔴 Key Required (Enter above or set in Streamlit Secrets)</span>", unsafe_allow_html=True)
        
    opt_model = "gemini-3-flash-preview"
            
    st.markdown("---")
    target = st.selectbox("Target Output Architecture", ["Gemini 3 Flash Optimized", "ChatGPT / GPT-4o", "Claude 3.5 Sonnet", "DeepSeek", "Llama 3", "Mistral"])
    style = st.selectbox("Optimization Style", ["Professional", "Technical", "Detailed", "Concise", "Beginner"])
    temperature = st.slider("Creativity / Temperature", 0.0, 1.0, 0.3)

if "optimized_prompt" not in st.session_state:
    st.session_state.optimized_prompt = ""

# --- Dual Workbench UI ---
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <span style="font-weight: 700; font-size: 1rem; color: #E2E8F0;">📝 Original Prompt</span>
        <span class="pf-badge">Input Workbench</span>
    </div>
    """, unsafe_allow_html=True)
    
    default_prompt = st.session_state.get("analyzer_to_optimizer_prompt", "")
    prompt = st.text_area(
        "Original Prompt",
        value=default_prompt,
        height=320,
        placeholder="Enter your raw prompt here... (e.g., Write a python script to parse CSV files and generate monthly sales summary)",
        label_visibility="collapsed"
    )
    
    if "analyzer_to_optimizer_prompt" in st.session_state:
        del st.session_state["analyzer_to_optimizer_prompt"]
        
    run = st.button("🚀 Forge & Optimize Prompt", use_container_width=True)

# --- Execution Logic ---
if run and prompt.strip():
    with st.spinner("Forging enterprise prompt with Gemini 3 Flash Preview..."):
        try:
            if not api_key:
                st.error("Please enter your Gemini API Key in the sidebar to activate the Gemini 3 Flash Preview optimizer.")
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
                result = generate_response(api_key, meta_prompt, opt_model)
        
            if result and not result.startswith("Error"):
                st.session_state.optimized_prompt = result
                from utils.history_manager import add_to_history
                from models.classifier import PromptClassifier
                from utils.scoring import score_prompt
                c = PromptClassifier().classify(result)
                s, _ = score_prompt(result)
                add_to_history(prompt, result, c.category, s, target, style)
            elif result.startswith("Error"):
                st.error(result)
        except Exception as e:
            st.error(f"Error optimizing prompt: {e}")

# --- Output UI ---
with c2:
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <span style="font-weight: 700; font-size: 1rem; color: #818CF8;">✨ Optimized Prompt</span>
        <span class="pf-badge" style="background: rgba(99,102,241,0.15); color: #C7D2FE;">Production Ready</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.text_area(
        "Optimized Prompt",
        value=st.session_state.optimized_prompt,
        height=320,
        label_visibility="collapsed"
    )
    
    if st.session_state.optimized_prompt:
        d1, d2 = st.columns(2)
        d1.download_button("📄 Download TXT", st.session_state.optimized_prompt, file_name="optimized_prompt.txt", use_container_width=True)
        try:
            from utils.pdf_generator import generate_pdf
            pdf_bytes = generate_pdf(st.session_state.optimized_prompt)
            d2.download_button("📑 Download PDF", pdf_bytes, file_name="optimized_prompt.pdf", mime="application/pdf", use_container_width=True)
        except Exception:
            d2.error("PDF generation unavailable")

st.divider()

# --- Analytics & Diagnostics ---
if prompt.strip():
    if not st.session_state.optimized_prompt:
        st.markdown("### 📊 Diagnostic Baseline (Original Prompt)")
        score, _ = score_prompt(prompt)
        cls = classifier.classify(prompt)
        ana = analyzer.analyze(prompt)
        stats = stats_engine.calculate(prompt)
        
        a, b, c, d = st.columns(4)
        a.metric("Clarity Score", f"{score}/100")
        b.metric("Domain Category", cls.category)
        c.metric("Confidence", f"{int(cls.confidence*100)}%")
        d.metric("Word Count", stats.word_count)
        
        st.progress(score/100, text=f"Baseline Quality: {score}%")
        
        st.markdown("### 💡 Recommended Enhancements")
        if ana.suggestions:
            for s in ana.suggestions:
                st.info(f"💡 {s}")
        else:
            st.success("Great prompt foundation! Ready for optimization.")
    else:
        st.markdown("### 📊 Comprehensive Optimization Delta")
        
        o_score, _ = score_prompt(prompt)
        o_cls = classifier.classify(prompt)
        o_stats = stats_engine.calculate(prompt)
        
        opt_score, _ = score_prompt(st.session_state.optimized_prompt)
        opt_cls = classifier.classify(st.session_state.optimized_prompt)
        opt_ana = analyzer.analyze(st.session_state.optimized_prompt)
        opt_stats = stats_engine.calculate(st.session_state.optimized_prompt)
        
        col_orig, col_opt = st.columns(2, gap="large")
        with col_orig:
            st.markdown("#### 📝 Original Baseline")
            st.metric("Quality Score", f"{o_score}/100")
            st.caption(f"Words: **{o_stats.word_count}** | Domain: **{o_cls.category}**")
            
        with col_opt:
            st.markdown("#### ✨ Optimized Quality")
            delta_val = opt_score - o_score
            delta_str = f"+{delta_val} points" if delta_val >= 0 else f"{delta_val} points"
            st.metric("Quality Score", f"{opt_score}/100", delta=delta_str)
            st.caption(f"Words: **{opt_stats.word_count}** | Domain: **{opt_cls.category}**")
            
        st.progress(opt_score/100, text=f"Optimized Quality: {opt_score}%")
        
        st.markdown("### 💡 Validation & Next Steps")
        if opt_ana.suggestions:
            for s in opt_ana.suggestions:
                st.info(f"💡 {s}")
        else:
            st.success("✨ This prompt has passed all structural guardrail checks and is ready to deploy!")

render_footer()
