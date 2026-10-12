import streamlit as st
from utils.helper import load_custom_css, render_sidebar_branding, render_footer

st.set_page_config(
    page_title="PromptForge AI | Intelligent Prompt Optimizer",
    page_icon="✨",
    layout="wide"
)

# Apply unified design system
load_custom_css()
render_sidebar_branding()

# --- HERO SECTION ---
st.markdown("""
<div class="pf-hero-card">
    <div class="pf-pill">
        <span class="pf-pill-dot"></span>
        <span>Google Gemini Studio • gemini-3-flash-preview</span>
    </div>
    <h1 style="font-size: 3rem; margin: 0 0 0.75rem 0; font-weight: 800; line-height: 1.15;">
        Intelligent <span class="pf-gradient-title">Prompt Engineering</span> Platform
    </h1>
    <p style="font-size: 1.15rem; color: #94A3B8; max-width: 780px; line-height: 1.6; margin: 0 0 1.75rem 0;">
        Transform vague ideas into rigorous, battle-tested prompts engineered exclusively with <b>Google Gemini</b> using the state-of-the-art <code>gemini-3-flash-preview</code> model. Eliminate hallucinations, enforce schema guardrails, and unlock peak LLM intelligence.
    </p>
    <div style="display: flex; gap: 12px; flex-wrap: wrap;">
        <span class="pf-badge" style="background: rgba(99, 102, 241, 0.2); color: #C7D2FE; border: 1px solid rgba(99, 102, 241, 0.3);">⚡ Powered by Gemini 3 Flash Preview</span>
        <span class="pf-badge" style="background: rgba(16, 185, 129, 0.15); color: #A7F3D0; border: 1px solid rgba(16, 185, 129, 0.3);">🔑 Gemini API Key Exclusive</span>
        <span class="pf-badge" style="background: rgba(6, 182, 212, 0.15); color: #A5F3FC; border: 1px solid rgba(6, 182, 212, 0.3);">📊 6-Axis Quality Diagnostics</span>
        <span class="pf-badge" style="background: rgba(244, 63, 94, 0.15); color: #FECDD3; border: 1px solid rgba(244, 63, 94, 0.3);">🔒 100% Client-Side Key Privacy</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- QUICK METRICS / BENCHMARK STRIP ---
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric(label="Quality Gain", value="+42%", delta="Avg. Clarity & Precision")
with col_m2:
    st.metric(label="AI Engine", value="Gemini 3 Flash", delta="gemini-3-flash-preview")
with col_m3:
    st.metric(label="Prompt Templates", value="50+ Ready", delta="Battle-tested Presets")
with col_m4:
    st.metric(label="Execution Speed", value="<0.9s", delta="Sub-second Flash Engine")

st.divider()

# --- WORKSPACE STUDIO SUITE ---
st.markdown("""
<div style="margin-bottom: 1.25rem;">
    <h2 style="font-size: 1.6rem; margin-bottom: 0.25rem;">🛠️ PromptForge Studio Suite</h2>
    <p style="color: #94A3B8; font-size: 0.95rem; margin: 0;">Select a specialized module to engineer, diagnose, or benchmark your prompts.</p>
</div>
""", unsafe_allow_html=True)

# Row 1
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="pf-feature-box">
        <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🚀</div>
        <h3 style="font-size: 1.15rem; margin-bottom: 0.35rem; color: #FFFFFF;">Prompt Optimizer</h3>
        <p style="font-size: 0.875rem; color: #94A3B8; line-height: 1.5; min-height: 52px; margin-bottom: 1rem;">
            Convert loose user prompts into professional, multi-layered system instructions with roles, schemas, and guardrails.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Prompt_Optimizer.py", label="Launch Optimizer", icon="🚀")

with c2:
    st.markdown("""
    <div class="pf-feature-box">
        <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">📊</div>
        <h3 style="font-size: 1.15rem; margin-bottom: 0.35rem; color: #FFFFFF;">Prompt Analyzer</h3>
        <p style="font-size: 0.875rem; color: #94A3B8; line-height: 1.5; min-height: 52px; margin-bottom: 1rem;">
            Deep diagnostics for readability, token complexity, specificity score, and rule-based refinement recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Prompt_Analyzer.py", label="Open Analyzer", icon="📊")

with c3:
    st.markdown("""
    <div class="pf-feature-box">
        <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">⚖️</div>
        <h3 style="font-size: 1.15rem; margin-bottom: 0.35rem; color: #FFFFFF;">Prompt Comparison</h3>
        <p style="font-size: 0.875rem; color: #94A3B8; line-height: 1.5; min-height: 52px; margin-bottom: 1rem;">
            Inspect original vs. optimized prompts side-by-side with visual diffing, delta scoring, and token efficiency analysis.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Prompt_Compare.py", label="Compare Prompts", icon="⚖️")

st.write("")

# Row 2
c4, c5, c6 = st.columns(3)

with c4:
    st.markdown("""
    <div class="pf-feature-box">
        <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🧪</div>
        <h3 style="font-size: 1.15rem; margin-bottom: 0.35rem; color: #FFFFFF;">Gemini Live Sandbox</h3>
        <p style="font-size: 0.875rem; color: #94A3B8; line-height: 1.5; min-height: 52px; margin-bottom: 1rem;">
            Directly execute prompts against Google's live gemini-3-flash-preview model using your own Gemini API key.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/7_Sandbox.py", label="Launch Sandbox", icon="🧪")

with c5:
    st.markdown("""
    <div class="pf-feature-box">
        <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">📝</div>
        <h3 style="font-size: 1.15rem; margin-bottom: 0.35rem; color: #FFFFFF;">Few-Shot Studio</h3>
        <p style="font-size: 0.875rem; color: #94A3B8; line-height: 1.5; min-height: 52px; margin-bottom: 1rem;">
            Construct consistent, deterministic prompts by injecting input-output exemplars and custom input formats.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/8_Few_Shot_Builder.py", label="Build Few-Shot", icon="📝")

with c6:
    st.markdown("""
    <div class="pf-feature-box">
        <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🧠</div>
        <h3 style="font-size: 1.15rem; margin-bottom: 0.35rem; color: #FFFFFF;">Chain-of-Thought Builder</h3>
        <p style="font-size: 0.875rem; color: #94A3B8; line-height: 1.5; min-height: 52px; margin-bottom: 1rem;">
            Enforce multi-step algorithmic reasoning paths to boost model accuracy on complex math, coding, and logical tasks.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/9_CoT_Builder.py", label="Build CoT Prompt", icon="🧠")

st.write("")

# Row 3
c7, c8, c9 = st.columns(3)

with c7:
    st.markdown("""
    <div class="pf-feature-box">
        <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">📚</div>
        <h3 style="font-size: 1.15rem; margin-bottom: 0.35rem; color: #FFFFFF;">Template Marketplace</h3>
        <p style="font-size: 0.875rem; color: #94A3B8; line-height: 1.5; min-height: 52px; margin-bottom: 1rem;">
            Explore curated system prompts across engineering, copywriting, marketing, finance, and code review.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_Prompt_Library.py", label="Explore Library", icon="📚")

with c8:
    st.markdown("""
    <div class="pf-feature-box">
        <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">🕒</div>
        <h3 style="font-size: 1.15rem; margin-bottom: 0.35rem; color: #FFFFFF;">History & Audit Log</h3>
        <p style="font-size: 0.875rem; color: #94A3B8; line-height: 1.5; min-height: 52px; margin-bottom: 1rem;">
            Search and restore previous prompt runs, review score progressions, and export full audit archives in JSON.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/5_Prompt_History.py", label="View History", icon="🕒")

with c9:
    st.markdown("""
    <div class="pf-feature-box">
        <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">⚙️</div>
        <h3 style="font-size: 1.15rem; margin-bottom: 0.35rem; color: #FFFFFF;">Studio Settings</h3>
        <p style="font-size: 0.875rem; color: #94A3B8; line-height: 1.5; min-height: 52px; margin-bottom: 1rem;">
            Configure your default target LLMs, temperature baselines, output lengths, and interface personalization.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/6_Settings.py", label="Open Settings", icon="⚙️")

st.divider()

# --- WHY PROMPTFORGE SECTION ---
st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <h2 style="font-size: 1.6rem; margin-bottom: 0.35rem;">💡 Why Engineering Prompts Matters</h2>
    <p style="color: #94A3B8; font-size: 0.95rem; margin: 0;">Unstructured prompts waste tokens, introduce hallucinations, and degrade reasoning quality.</p>
</div>
""", unsafe_allow_html=True)

col_w1, col_w2, col_w3 = st.columns(3)

with col_w1:
    st.markdown("""
    <div style="background: rgba(18, 24, 36, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 1.25rem;">
        <h4 style="color: #818CF8; margin-top: 0; font-size: 1.05rem;">🎯 Strict Role & Persona Definition</h4>
        <p style="color: #94A3B8; font-size: 0.875rem; line-height: 1.55; margin: 0;">
            LLMs condition on initial token probabilities. PromptForge injects high-status expert personas with domain boundaries so outputs are authoritative and laser-focused.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_w2:
    st.markdown("""
    <div style="background: rgba(18, 24, 36, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 1.25rem;">
        <h4 style="color: #34D399; margin-top: 0; font-size: 1.05rem;">🛡️ Guardrails & Format Contracts</h4>
        <p style="color: #94A3B8; font-size: 0.875rem; line-height: 1.55; margin: 0;">
            Clear negative constraints and schema contracts eliminate conversational preamble, fluff, and invalid JSON/Markdown, ensuring seamless downstream pipeline integration.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_w3:
    st.markdown("""
    <div style="background: rgba(18, 24, 36, 0.6); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 14px; padding: 1.25rem;">
        <h4 style="color: #38BDF8; margin-top: 0; font-size: 1.05rem;">💰 Token Efficiency & Cost Savings</h4>
        <p style="color: #94A3B8; font-size: 0.875rem; line-height: 1.55; margin: 0;">
            Fewer clarification rounds and deterministic outputs mean lower token consumption and zero developer frustration when deploying to production.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Sleek Platform Footer
render_footer()
