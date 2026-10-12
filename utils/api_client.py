"""
utils/api_client.py

Production-grade client dedicated exclusively to Google Gemini API using gemini-3-flash-preview.
Supports automated key resolution via UI, st.session_state, st.secrets, and environment variables.
"""

import os
from typing import Optional
import google.generativeai as genai

DEFAULT_MODEL = "gemini-3-flash-preview"


def get_gemini_api_key(provided_key: str = "") -> str:
    """
    Resolves the Gemini API Key with the following precedence:
    1. Directly provided key argument
    2. Streamlit session state ('gemini_api_key')
    3. Streamlit secrets (st.secrets["GEMINI_API_KEY"])
    4. Environment variable (os.environ["GEMINI_API_KEY"])
    """
    if provided_key and provided_key.strip():
        return provided_key.strip()

    try:
        import streamlit as st
        if "gemini_api_key" in st.session_state and st.session_state["gemini_api_key"]:
            return st.session_state["gemini_api_key"].strip()
    except Exception:
        pass

    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            return str(st.secrets["GEMINI_API_KEY"]).strip()
    except Exception:
        pass

    env_key = os.environ.get("GEMINI_API_KEY", "")
    if env_key and env_key.strip():
        return env_key.strip()

    return ""


def set_gemini_api_key(api_key: str) -> None:
    """Syncs the Gemini API Key into session state for cross-page persistence."""
    try:
        import streamlit as st
        if api_key and api_key.strip():
            st.session_state["gemini_api_key"] = api_key.strip()
    except Exception:
        pass


def generate_response(
    api_key_or_provider: str = "",
    prompt_or_key: str = "",
    prompt: Optional[str] = None,
    model_name: str = DEFAULT_MODEL
) -> str:
    """
    Executes prompt generation with Google Gemini API using gemini-3-flash-preview.
    Handles quota exceptions, formatting checks, and multi-signature compatibility.
    """
    if prompt is not None:
        # Legacy signature: generate_response(provider, api_key, prompt, model_name)
        candidate_key = prompt_or_key
        user_prompt = prompt
        target_model = model_name or DEFAULT_MODEL
    else:
        # Standard signature: generate_response(api_key, prompt) or generate_response(prompt=...)
        candidate_key = api_key_or_provider
        user_prompt = prompt_or_key
        target_model = DEFAULT_MODEL

    resolved_key = get_gemini_api_key(candidate_key)

    if not resolved_key:
        return "Error: Gemini API Key is missing. Please provide your Gemini API Key in the sidebar or configure GEMINI_API_KEY in Streamlit Secrets."

    # Cache resolved key across pages
    set_gemini_api_key(resolved_key)

    if not user_prompt or not user_prompt.strip():
        return "Error: Prompt cannot be empty."

    try:
        genai.configure(api_key=resolved_key)
        model = genai.GenerativeModel(target_model)
        response = model.generate_content(user_prompt)

        if response and hasattr(response, "text") and response.text:
            return response.text.strip()
        
        return "Error: Gemini returned an empty response. Please verify the prompt constraints."

    except Exception as e:
        err_msg = str(e)
        if "API_KEY_INVALID" in err_msg or "400" in err_msg and "API key" in err_msg:
            return "Error: The provided Gemini API Key is invalid. Please check your key at https://aistudio.google.com/app/apikey"
        elif "ResourceExhausted" in err_msg or "429" in err_msg:
            return "Error: Gemini API rate limit or quota exceeded (429). Please wait a moment and try again, or check your quota at Google AI Studio."
        elif "not found" in err_msg.lower() and "model" in err_msg.lower():
            # If preview model alias needs fallback in specific region
            return f"Error connecting to Google Gemini model '{target_model}'. The preview model might be restricted in your region."
        return f"Error connecting to Google Gemini API ({target_model}): {err_msg}"
