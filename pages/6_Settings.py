import json
from pathlib import Path
import streamlit as st
from utils.helper import load_custom_css, render_sidebar_branding, render_page_header, render_footer

# Page Config
st.set_page_config(
    page_title="Settings | PromptForge AI",
    page_icon="⚙️",
    layout="wide"
)

load_custom_css()
render_sidebar_branding()


# File Paths


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

SETTINGS_FILE = DATA_DIR / "settings.json"

DEFAULT_SETTINGS = {

    "target_model": "Gemini 3 Flash Preview",

    "optimization_style": "Professional",

    "temperature": 0.3,

    "max_tokens": 256,

    "auto_save_history": True,

    "show_statistics": True,

    "show_evaluation": True,

    "theme": "Dark"

}

# Helpers


def load_settings():

    if SETTINGS_FILE.exists():

        try:

            with open(
                SETTINGS_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return DEFAULT_SETTINGS.copy()

    return DEFAULT_SETTINGS.copy()


def save_settings(settings):

    with open(
        SETTINGS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            settings,
            f,
            indent=4
        )


settings = load_settings()


# UI


render_page_header(
    title="Studio Settings",
    subtitle="Configure default target LLMs, temperature baselines, output parameters, and behavior.",
    icon="⚙️",
    badge="SYSTEM CONFIG"
)

st.divider()

# AI Model


st.subheader("🤖 AI Configuration")

model_options = [
    "Gemini 3 Flash Preview",
    "ChatGPT",
    "Claude",
    "DeepSeek",
    "Llama",
    "Mistral"
]
current_model = settings.get("target_model", "Gemini 3 Flash Preview")
if current_model not in model_options:
    current_model = "Gemini 3 Flash Preview"

settings["target_model"] = st.selectbox(
    "Default Target Model",
    model_options,
    index=model_options.index(current_model)
)

settings["optimization_style"] = st.selectbox(

    "Default Optimization Style",

    [

        "Professional",

        "Technical",

        "Detailed",

        "Concise",

        "Beginner"

    ],

    index=[

        "Professional",

        "Technical",

        "Detailed",

        "Concise",

        "Beginner"

    ].index(settings["optimization_style"])

)

settings["temperature"] = st.slider(

    "Creativity (Temperature)",

    0.0,

    1.0,

    float(settings["temperature"]),

    0.1

)

settings["max_tokens"] = st.slider(

    "Maximum Output Tokens",

    64,

    1024,

    int(settings["max_tokens"]),

    32

)

st.divider()

# Display


st.subheader("🖥 Interface")

settings["theme"] = st.selectbox(

    "Theme",

    [

        "Dark",

        "Light"

    ],

    index=0 if settings["theme"] == "Dark" else 1

)

settings["show_statistics"] = st.checkbox(

    "Show Prompt Statistics",

    value=settings["show_statistics"]

)

settings["show_evaluation"] = st.checkbox(

    "Show AI Evaluation",

    value=settings["show_evaluation"]

)

settings["auto_save_history"] = st.checkbox(

    "Automatically Save Prompt History",

    value=settings["auto_save_history"]

)

st.divider()

# Save / Reset


col1, col2 = st.columns(2)

with col1:

    if st.button(

        "💾 Save Settings",

        use_container_width=True

    ):

        save_settings(settings)

        st.success("Settings saved successfully!")

with col2:

    if st.button(

        "🔄 Reset to Default",

        use_container_width=True

    ):

        save_settings(DEFAULT_SETTINGS)

        st.success("Settings restored to default.")

        st.rerun()

st.divider()


# Current Settings


with st.expander("📄 Current Configuration"):

    st.json(settings)

render_footer()