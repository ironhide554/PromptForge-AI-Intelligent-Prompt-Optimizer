# ✨ PromptForge AI – Intelligent Prompt Optimizer

<div align="center">

# PromptForge AI
### Production-Grade Enterprise Prompt Studio powered by Google Gemini `gemini-3-flash-preview`

Transform simple, ambiguous inputs into high-precision, production-ready prompts with role definitions, schema contracts, and negative guardrails.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)](https://python.org)
[![Google Gemini](https://img.shields.io/badge/Engine-Gemini%203%20Flash%20Preview-4285F4.svg?logo=google&logoColor=white)](https://aistudio.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI Tests](https://img.shields.io/badge/Tests-20%20Passing-brightgreen.svg)]()

</div>

---

## 📌 Overview

**PromptForge AI** is an intelligent prompt engineering platform. It evaluates, refines, and formats prompts using Google's ultra-fast reasoning model **`gemini-3-flash-preview`** via a secure **Bring-Your-Own-Key (BYOK)** architecture.

Keys can be provided via the UI sidebar, `.env` file, or Streamlit Cloud Secrets with **zero persistence** across server disks.

---

## 🛠️ Complete Feature Suite

| Module | Location | Description |
|---|---|---|
| **🚀 Prompt Optimizer** | [`pages/1_Prompt_Optimizer.py`](pages/1_Prompt_Optimizer.py) | Cloud AI structural rewriting into personas, constraints, and schemas. |
| **📊 Prompt Analyzer** | [`pages/2_Prompt_Analyzer.py`](pages/2_Prompt_Analyzer.py) | 6-axis quality diagnostic breakdown, letter grade (`A+` to `F`), and token costs. |
| **⚖️ Prompt Compare** | [`pages/3_Prompt_Compare.py`](pages/3_Prompt_Compare.py) | Side-by-side line diffing, lexical growth, and quality score delta. |
| **📚 Template Library** | [`pages/4_Prompt_Library.py`](pages/4_Prompt_Library.py) | Built-in system templates, custom template creation, and community marketplace. |
| **🕒 Audit History** | [`pages/5_Prompt_History.py`](pages/5_Prompt_History.py) | Semantic & keyword prompt search, version rollback, and JSON export. |
| **⚙️ Studio Settings** | [`pages/6_Settings.py`](pages/6_Settings.py) | Global defaults, temperature tuning, and system JSON configuration. |
| **🧪 Gemini Sandbox** | [`pages/7_Sandbox.py`](pages/7_Sandbox.py) | Live interactive execution against `gemini-3-flash-preview`. |
| **📝 Few-Shot Studio** | [`pages/8_Few_Shot_Builder.py`](pages/8_Few_Shot_Builder.py) | In-context exemplar builder with one-click live execution. |
| **🧠 CoT Builder** | [`pages/9_CoT_Builder.py`](pages/9_CoT_Builder.py) | Step-by-step reasoning pipeline constructor with live test runner. |

---

## 🏗️ Architecture & Directory Structure

```text
PromptForge-AI/
├── app.py                     # Main dashboard landing & hero overview
├── assets/
│   └── style.css              # Obsidian slate dark theme & SaaS design system
├── .streamlit/
│   ├── config.toml            # Theme and server configuration
│   └── secrets.toml.example   # Secrets template for Streamlit Cloud
├── models/
│   ├── analyzer.py            # Rule-based prompt syntax parser
│   ├── classifier.py          # Domain classification engine
│   └── evaluator.py           # Letter grade and AI readiness evaluator
├── pages/
│   ├── 1_Prompt_Optimizer.py
│   ├── 2_Prompt_Analyzer.py
│   ├── 3_Prompt_Compare.py
│   ├── 4_Prompt_Library.py
│   ├── 5_Prompt_History.py
│   ├── 6_Settings.py
│   ├── 7_Sandbox.py
│   ├── 8_Few_Shot_Builder.py
│   └── 9_CoT_Builder.py
├── utils/
│   ├── api_client.py          # Gemini 3 Flash Preview client & key resolver
│   ├── embeddings.py          # Semantic similarity search using sentence embeddings
│   ├── helper.py              # Brand header/footer and design system loader
│   ├── history_manager.py     # JSON history manager
│   ├── pdf_generator.py       # PDF artifact compiler
│   ├── prompt_stats.py        # Token, word, and readability calculations
│   ├── scoring.py             # 100-point quality evaluation algorithm
│   └── templates.py           # Template manager & persistence
├── tests/                     # 20 unit tests with 100% pass rate
├── Dockerfile                 # Multi-platform container configuration
├── requirements.txt           # Verified dependency manifest
└── .env.example               # Environment variables template
```

---

## 🚀 Quickstart & Local Setup

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/yourusername/PromptForge-AI.git
cd PromptForge-AI

# Create virtual environment
python -m venv .venv

# Activate on Windows
.venv\Scripts\activate

# Activate on macOS/Linux
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API Key (Optional)

Create a `.env` file from the template:

```bash
cp .env.example .env
```

Add your Gemini API Key in `.env`:
```env
GEMINI_API_KEY="AIzaSy..."
```

*(You can also simply enter your key inside the app sidebar at runtime!)*

### 4. Run the Platform

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🧪 Running the Test Suite

Run all 20 automated unit tests with `pytest`:

```bash
pytest tests/ -v
```

---

## 🌐 1-Click Deployment Guide

### Deploying to Streamlit Community Cloud (Recommended)

1. Push your repository to **GitHub**.
2. Visit [share.streamlit.io](https://share.streamlit.io) and click **"New app"**.
3. Select your repository, branch (`main`), and set **Main file path** to `app.py`.
4. Under **Advanced Settings → Secrets**, paste your key:
   ```toml
   GEMINI_API_KEY = "your_actual_gemini_api_key_here"
   ```
5. Click **Deploy!** Your live application URL will be generated in under 60 seconds.

---

### Deploying via Docker

```bash
# Build the container image
docker build -t promptforge-ai:latest .

# Run container on port 8501
docker run -d -p 8501:8501 -e GEMINI_API_KEY="your_key" --name promptforge promptforge-ai:latest
```

Access at `http://localhost:8501`.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
