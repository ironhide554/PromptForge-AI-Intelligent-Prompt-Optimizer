import streamlit as st
from models.analyzer import PromptAnalyzer
from models.classifier import PromptClassifier
from models.evaluator import PromptEvaluator
from utils.scoring import score_prompt
from utils.prompt_stats import PromptStats
from utils.helper import load_custom_css, render_sidebar_branding, render_page_header, render_footer


st.set_page_config(
    page_title="Prompt Analyzer | PromptForge AI",
    page_icon="📊",
    layout="wide"
)

load_custom_css()
render_sidebar_branding()

# ----------------------------------------------------
# Load Models
# ----------------------------------------------------

analyzer = PromptAnalyzer()
classifier = PromptClassifier()
stats_engine = PromptStats()
evaluator = PromptEvaluator()

# ----------------------------------------------------
# Header
# ----------------------------------------------------

render_page_header(
    title="Prompt Analyzer",
    subtitle="Evaluate prompt quality, lexical density, readability scores, and structural components.",
    icon="📊",
    badge="DIAGNOSTICS & AUDIT"
)

st.divider()

# ----------------------------------------------------
# Input
# ----------------------------------------------------

prompt = st.text_area(
    "Enter your Prompt",
    height=220,
    placeholder="Example: Build a Streamlit dashboard using Random Forest..."
)

analyze_button = st.button(
    "Analyze Prompt",
    use_container_width=True
)

# ----------------------------------------------------
# Analysis
# ----------------------------------------------------

if analyze_button:

    if not prompt.strip():

        st.warning("Please enter a prompt.")

        st.stop()

    analysis = analyzer.analyze(prompt)

    evaluation = evaluator.evaluate(prompt)
    category = classifier.classify(prompt)
    score, score_suggestions = score_prompt(prompt)
    statistics = stats_engine.calculate(prompt)

    # ------------------------------------------

    st.success("Analysis Completed Successfully")

    st.divider()

    # ------------------------------------------
    # Top Metrics
    # ------------------------------------------

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Overall Score",
        f"{evaluation.score}/100"
    )

    c2.metric(
        "Letter Grade",
        evaluation.grade
    )

    c3.metric(
        "Production Ready",
        "Ready ✅" if evaluation.ai_ready else "Needs Work ⚠️"
    )

    c4.metric(
        "Category",
        evaluation.category
    )

    c5.metric(
        "Complexity",
        evaluation.complexity
    )

    st.progress(
        evaluation.score / 100,
        text=f"Diagnostic Quality Score: {evaluation.score}%"
    )

    st.info(f"📋 **Evaluation Summary:** {evaluation.summary}")

    st.divider()

    st.subheader("🔍 Prompt Syntax Highlight")
    st.caption("Key prompt engineering elements are highlighted below.")
    
    highlighted_text = prompt
    
    # Simple highlighter helper
    def highlight_words(text, words, color):
        import re
        for w in words:
            # Case insensitive exact word match
            text = re.sub(rf'\b({w})\b', rf'<span style="background-color: {color}; color: white; padding: 2px 4px; border-radius: 4px; font-weight: bold;">\1</span>', text, flags=re.IGNORECASE)
        return text

    highlighted_text = highlight_words(highlighted_text, analyzer.ACTION_VERBS, "#FF4B4B") # Red - Actions
    highlighted_text = highlight_words(highlighted_text, analyzer.PERSONA_WORDS, "#0068C9") # Blue - Personas
    highlighted_text = highlight_words(highlighted_text, analyzer.CONSTRAINT_WORDS, "#29B09D") # Teal - Constraints
    highlighted_text = highlight_words(highlighted_text, analyzer.FORMAT_WORDS, "#FF8700") # Orange - Formats
    
    st.markdown(
        f'<div style="background-color: rgba(18, 24, 36, 0.85); border: 1px solid rgba(255, 255, 255, 0.1); padding: 18px; border-radius: 14px; color: #F1F5F9; font-size: 15px; font-family: \'JetBrains Mono\', monospace; line-height: 1.8; box-shadow: inset 0 2px 6px rgba(0,0,0,0.3);">{highlighted_text.replace(chr(10), "<br>")}</div>',
        unsafe_allow_html=True
    )
    
    st.markdown(
        '<div style="margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap;">'
        '<span style="background-color: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.4); color: #FCA5A5; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 600;">⚡ Action</span>'
        '<span style="background-color: rgba(99, 102, 241, 0.2); border: 1px solid rgba(99, 102, 241, 0.4); color: #C7D2FE; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 600;">👤 Persona</span>'
        '<span style="background-color: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); color: #A7F3D0; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 600;">🛡️ Constraint</span>'
        '<span style="background-color: rgba(245, 158, 11, 0.2); border: 1px solid rgba(245, 158, 11, 0.4); color: #FDE68A; padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 600;">📋 Format</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # ------------------------------------------
    # Detailed Scores
    # ------------------------------------------

    st.subheader("Quality Breakdown")

    import pandas as pd
    chart_data = pd.DataFrame(
        {
            "Metric": ["Clarity", "Context", "Specificity", "Persona", "Constraints", "Format"],
            "Score %": [
                (analysis.clarity_score / 20) * 100,
                (analysis.context_score / 20) * 100,
                (analysis.specificity_score / 15) * 100,
                (analysis.persona_score / 15) * 100,
                (analysis.constraints_score / 15) * 100,
                (analysis.format_score / 15) * 100
            ]
        }
    ).set_index("Metric")
    
    st.bar_chart(chart_data, y="Score %", height=300)

    st.divider()

    # ------------------------------------------
    # Prompt Statistics
    # ------------------------------------------

    st.subheader("📈 Prompt Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Words",
        statistics.word_count
    )

    col1.metric(
        "Characters",
        statistics.character_count
    )

    col1.metric(
        "Paragraphs",
        statistics.paragraph_count
    )

    col2.metric(
        "Sentences",
        statistics.sentence_count
    )

    col2.metric(
        "Estimated Tokens",
        statistics.estimated_tokens
    )

    col2.metric(
        "Reading Time",
        f"{statistics.estimated_reading_time} min"
    )

    col3.metric(
        "Readability",
        statistics.readability
    )

    col3.metric(
        "Lexical Diversity",
        statistics.lexical_diversity
    )

    col3.metric(
        "Density",
        statistics.prompt_density
    )

    st.markdown("##### ⚡ Gemini 3 Flash Preview Token Cost")
    
    gemini_cost = (statistics.estimated_tokens / 1_000_000) * 0.15
    
    p1, p2, p3 = st.columns(3)
    p1.metric("Engine Model", "gemini-3-flash-preview")
    p2.metric("Estimated Cost (Input)", f"${gemini_cost:.6f}")
    p3.metric("Estimated Tokens", f"{statistics.estimated_tokens}", delta="Ultra-efficient")

    st.divider()

    # ------------------------------------------
    # Strengths & Weaknesses
    # ------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("✅ Strengths")

        if analysis.strengths:

            for strength in analysis.strengths:

                st.success(strength)

        else:

            st.info("No strengths detected.")

    with col2:

        st.subheader("❌ Weaknesses")

        if analysis.weaknesses:

            for weakness in analysis.weaknesses:

                st.error(weakness)

        else:

            st.success("No weaknesses detected.")

    st.divider()

    # ------------------------------------------
    # Suggestions
    # ------------------------------------------

    st.subheader("💡 Improvement Suggestions")

    suggestions = list(
        dict.fromkeys(
            analysis.suggestions
        )
    )

    if suggestions:

        for suggestion in suggestions:

            st.info(suggestion)

    else:

        st.success(
            "Excellent prompt. No improvements required."
        )

    st.divider()

    # ------------------------------------------
    # Matched Keywords
    # ------------------------------------------

    st.subheader("🏷️ Detected Keywords")

    if category.matched_keywords:

        cols = st.columns(4)

        for i, keyword in enumerate(category.matched_keywords):

            cols[i % 4].success(keyword)

    else:

        st.info("No category keywords detected.")

    st.divider()

    # ------------------------------------------
    # Overall Recommendation
    # ------------------------------------------

    st.subheader("🎯 Recommendation")

    if score >= 90:
        st.success("Excellent prompt. Ready for production use.")
    elif score >= 75:
        st.success("Very good prompt. Minor improvements recommended.")
    elif score >= 55:
        st.warning("Average prompt. Consider adding more context and constraints.")
    else:
        st.error("Weak prompt. It should be rewritten before using with an LLM.")

    if st.button("🚀 Send to Optimizer", use_container_width=True, type="primary"):
        st.session_state.analyzer_to_optimizer_prompt = prompt
        st.switch_page("pages/1_Prompt_Optimizer.py")

    st.divider()

    # Generate Report String
    report = f"""Prompt Analysis Report
======================

Original Prompt:
{prompt}

Overall Score: {score}/100
Category: {category.category}
Complexity: {analysis.complexity}

Quality Breakdown:
- Clarity: {analysis.clarity_score}/20
- Context: {analysis.context_score}/20
- Specificity: {analysis.specificity_score}/15
- Persona: {analysis.persona_score}/15
- Constraints: {analysis.constraints_score}/15
- Format: {analysis.format_score}/15

Statistics:
- Words: {statistics.word_count}
- Tokens: {statistics.estimated_tokens}
- Readability: {statistics.readability}

Estimated API Cost:
- Model: Google Gemini 3 Flash Preview (gemini-3-flash-preview)
- Estimated Input Cost: ${gemini_cost:.6f}
"""

    st.download_button(
        label="📥 Download Full Analysis Report",
        data=report,
        file_name="prompt_analysis_report.txt",
        mime="text/plain",
        use_container_width=True
    )

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

render_footer()