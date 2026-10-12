import unittest
import os
from utils.api_client import get_gemini_api_key, set_gemini_api_key, generate_response, DEFAULT_MODEL

class TestApiClient(unittest.TestCase):
    def setUp(self):
        try:
            import streamlit as st
            if "gemini_api_key" in st.session_state:
                del st.session_state["gemini_api_key"]
        except Exception:
            pass
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]

    def tearDown(self):
        try:
            import streamlit as st
            if "gemini_api_key" in st.session_state:
                del st.session_state["gemini_api_key"]
        except Exception:
            pass
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]

    def test_default_model_is_gemini_3_flash_preview(self):
        self.assertEqual(DEFAULT_MODEL, "gemini-3-flash-preview")

    def test_missing_api_key_returns_error(self):
        res = generate_response(api_key_or_provider="", prompt_or_key="Test prompt")
        self.assertTrue(res.startswith("Error: Gemini API Key is missing"))

    def test_empty_prompt_returns_error(self):
        res = generate_response(api_key_or_provider="fake-key", prompt_or_key="")
        self.assertTrue(res.startswith("Error: Prompt cannot be empty"))

    def test_key_resolution_precedence(self):
        key = get_gemini_api_key(provided_key="my_explicit_key")
        self.assertEqual(key, "my_explicit_key")

if __name__ == "__main__":
    unittest.main()
