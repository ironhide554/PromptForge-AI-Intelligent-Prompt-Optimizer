import streamlit as st
from utils.api_client import generate_response
from utils.helper import load_custom_css, render_sidebar_branding, render_page_header, render_footer

st.set_page_config(
    page_title="API Sandbox | PromptForge AI",
    page_icon="🧪",
    layout="wide"
)

load_custom_css()
render_sidebar_branding()

render_page_header(
    title="Gemini 3 Flash Preview Sandbox",
    subtitle="Test your optimized prompts directly against Google's gemini-3-flash-preview model using your own Gemini API key.",
    icon="🧪",
    badge="GEMINI 3 FLASH LAB"
)

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("### ⚡ Gemini Engine Setup")
    
    st.markdown("""
    <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 12px; padding: 14px; margin-bottom: 14px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: #6366F1; display: inline-block;"></span>
            <span style="font-weight: 700; font-size: 0.9rem; color: #A5B4FC;">Google Gemini 3 Flash Preview</span>
        </div>
        <p style="font-size: 0.775rem; color: #94A3B8; margin: 0; line-height: 1.4;">
            Active Model: <code style="color: #E2E8F0;">gemini-3-flash-preview</code>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    from utils.api_client import get_gemini_api_key, set_gemini_api_key
    cached_key = get_gemini_api_key()

    api_key = st.text_input(
        "Gemini API Key",
        value=cached_key,
        type="password",
        help="Enter your Google Gemini API key. Auto-resolved from Secrets, .env, or active session.",
        placeholder="AIzaSy..."
    )
    if api_key:
        set_gemini_api_key(api_key)
        st.markdown("<span style='color: #34D399; font-size: 0.75rem;'>🟢 Gemini Key Ready</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span style='color: #F87171; font-size: 0.75rem;'>🔴 Key Required (Enter above or set in Streamlit Secrets)</span>", unsafe_allow_html=True)
        
    model_name = "gemini-3-flash-preview"
        
    st.markdown("""
    <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 10px; padding: 12px; margin-top: 10px;">
        <span style="font-size: 0.8rem; color: #94A3B8;">🔒 <b>Zero Persistence:</b> Your Gemini API key is used strictly for this request via TLS directly to Google API endpoints.</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📝 Prompt Execution Workbench")
    
    default_prompt = st.session_state.get("optimized", "")
    if not default_prompt and "optimized_prompt" in st.session_state:
        default_prompt = st.session_state.optimized_prompt
    
    user_prompt = st.text_area(
        "Enter Prompt to test",
        value=default_prompt,
        height=220,
        placeholder="Paste your prompt here to execute live against Gemini 3 Flash Preview...",
        label_visibility="collapsed"
    )
    
    test_btn = st.button("🚀 Execute Live Prompt (Gemini 3 Flash Preview)", use_container_width=True, type="primary")

st.divider()

if test_btn:
    if not api_key:
        st.error("Please enter your Gemini API Key in the left panel to execute this prompt.")
    elif not user_prompt.strip():
        st.warning("Please enter a prompt to test.")
    else:
        st.markdown(f"### 🤖 Live Output from `gemini-3-flash-preview`")
        with st.spinner("Connecting to Google Gemini (gemini-3-flash-preview)..."):
            response = generate_response(api_key, user_prompt, model_name)
            
            if response.startswith("Error"):
                st.error(response)
            else:
                with st.chat_message("assistant"):
                    st.markdown(response)

render_footer()
