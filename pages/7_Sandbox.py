import streamlit as st
from utils.api_client import generate_response

st.set_page_config(
    page_title="API Sandbox",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Live API Sandbox")
st.markdown("Test your optimized prompts directly against live LLMs using your own API keys. (Your keys are never saved!)")

st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("⚙️ Setup")
    provider = st.selectbox(
        "Select Provider",
        ["OpenAI", "Anthropic", "Google Gemini"]
    )
    
    if provider == "OpenAI":
        model_name = st.selectbox("Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"])
    elif provider == "Anthropic":
        model_name = st.selectbox("Model", ["claude-3-5-sonnet-20240620", "claude-3-opus-20240229", "claude-3-haiku-20240307"])
    else:
        model_name = st.selectbox("Model", ["gemini-1.5-pro", "gemini-1.5-flash"])
        
    api_key = st.text_input(
        f"{provider} API Key",
        type="password",
        placeholder="sk-..."
    )
    
    st.info("Don't have a key? Get one from the developer console of the respective provider.")

with col2:
    st.subheader("📝 Prompt Testing")
    
    # Retrieve optimized prompt from session state if available
    default_prompt = st.session_state.get("optimized", "")
    
    user_prompt = st.text_area(
        "Enter Prompt to test",
        value=default_prompt,
        height=200,
        placeholder="Paste your optimized prompt here..."
    )
    
    test_btn = st.button("🚀 Run Prompt", use_container_width=True, type="primary")

st.divider()

if test_btn:
    if not api_key:
        st.error("Please enter your API Key to test the prompt.")
    elif not user_prompt.strip():
        st.warning("Please enter a prompt to test.")
    else:
        st.subheader("🤖 AI Response")
        with st.spinner(f"Sending to {model_name}..."):
            response = generate_response(provider, api_key, user_prompt, model_name)
            
            if response.startswith("Error"):
                st.error(response)
            else:
                # Display output as a simulated chat
                with st.chat_message("assistant"):
                    st.markdown(response)
