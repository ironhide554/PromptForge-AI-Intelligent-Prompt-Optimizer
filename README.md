# ✨ PromptForge AI Intelligent Prompt Optimizer

<div align="center">

# PromptForge AI

### Intelligent Prompt Optimizer using Cloud AI (BYOK)

Transform simple prompts into structured, high-quality prompts for ChatGPT, Claude, Gemini, DeepSeek, Llama, and other Large Language Models.

Built with **Streamlit** and powered by **OpenAI, Anthropic, and Google Gemini APIs**.

---

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![BYOK](https://img.shields.io/badge/Architecture-BYOK-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

# 📌 Overview

PromptForge AI is an intelligent prompt optimization system that helps users convert vague prompts into detailed, structured, and high-quality prompts suitable for modern Large Language Models (LLMs).

The application uses a **Bring-Your-Own-Key (BYOK)** architecture, allowing you to connect securely to OpenAI, Anthropic, or Google Gemini. It uses these state-of-the-art models as "Expert Prompt Engineers" to analyze prompt quality, provide actionable improvement suggestions, calculate a quality score, and generate highly optimized prompts.

---

# 🚀 Features

## ✅ Prompt Optimization

Convert basic prompts into professional prompts.

Example

Input

```text
Write a resume
```

Output

```text
Act as an experienced technical recruiter.

Create an ATS-friendly resume for a Machine Learning Engineer.

Requirements:
• Highlight measurable achievements
• Use professional formatting
• Keep it under two pages
• Output in Markdown
```

---

## 📊 Prompt Quality Score

Every prompt receives a score out of 100 based on:

* Context
* Specificity
* Constraints
* Role Assignment
* Output Format
* Prompt Length
* Examples
* Goal Clarity

---

## 💡 Smart Suggestions

The system identifies missing prompt components and recommends improvements.

Example:

* Add context
* Specify the output format
* Define the AI role
* Add constraints
* Provide examples

---

## 🎯 Target Model Selection

Optimize prompts specifically for

* ChatGPT
* Claude
* Gemini
* DeepSeek
* Llama
* Mistral

---

## 📥 Export Prompt

Download the optimized prompt as a text file.

---

# 🏗️ Project Structure

```text
PromptForge-AI/
│
├── app.py
│
├── models/
│   └── optimizer.py
│
├── utils/
│   ├── scoring.py
│   └── helpers.py
│
├── assets/
│   └── style.css
│
├── requirements.txt
│
└── README.md
```

---

# 🧠 Tech Stack

## Frontend

* Streamlit

## Backend

* Python

## AI Integrations (BYOK)

* OpenAI API
* Anthropic API
* Google Gemini API

## Libraries

* openai
* anthropic
* google-generativeai
* pytest

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/PromptForge-AI.git
```

Go to the project directory

```bash
cd PromptForge-AI
```

Create a virtual environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

Run tests

```bash
pytest tests/
```

---

# 📈 Workflow

```text
User Prompt + Selected Target & Style
      │
      ▼
Prompt Analysis & Scoring
      │
      ▼
Cloud AI API (OpenAI/Anthropic/Gemini)
      │
      ▼
Optimized Prompt & Final Scoring
      │
      ▼
Download Result
```

---

# 📷 Screenshots

Add screenshots here after running the project.

```
screenshots/

home.png

optimized_prompt.png

prompt_score.png
```

---

# 📊 Example

Original Prompt

```text
Explain AI
```

Optimized Prompt

```text
Act as an experienced AI professor.

Explain Artificial Intelligence to a beginner.

Requirements:

• Use simple language
• Include real-world examples
• Compare AI with Machine Learning
• End with key takeaways
• Output using Markdown headings
```

---

# 🎯 Future Roadmap

## Phase 1

* Prompt Optimizer
* Prompt Score
* Prompt Suggestions

## Phase 2

* Prompt Type Detection
* Prompt Comparison
* Prompt Analyzer

## Phase 3

* Prompt Library
* Prompt History
* SQLite Integration
* Export PDF

## Phase 4

* Embeddings Search
* Few-shot Prompt Generation
* Chain-of-Thought Builder
* Token Estimation
* Prompt Templates Marketplace

---

# 💼 Skills Demonstrated

* Prompt Engineering
* Transformer Models
* Natural Language Processing
* Streamlit
* Hugging Face
* PyTorch
* Model Inference
* Text Generation
* AI Application Development
* Software Engineering

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository

2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add feature"
```

4. Push your branch

```bash
git push origin feature-name
```

5. Create a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# ⭐ Support

If you found this project helpful:

⭐ Star the repository

🍴 Fork the repository

🛠️ Contribute to the project

---

<div align="center">

Made with ❤️ using Streamlit and Hugging Face Transformers

</div>
