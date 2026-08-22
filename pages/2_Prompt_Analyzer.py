import streamlit as st

from models.analyzer import PromptAnalyzer
from models.classifier import PromptClassifier
from utils.scoring import score_prompt
from utils.prompt_stats import PromptStats


st.set_page_config(
    page_title="Prompt Analyzer",
    page_icon="📊",
    layout="wide"
)

# ----------------------------------------------------
# Load Models
# ----------------------------------------------------

analyzer = PromptAnalyzer()
classifier = PromptClassifier()
stats_engine = PromptStats()

# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.title("📊 Prompt Analyzer")

st.markdown(
"""
Analyze your prompt before sending it to an LLM.

The analyzer evaluates:

- Prompt Quality
- Category
- Statistics
- Readability
- Complexity
- Suggestions
"""
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

    category = classifier.classify(prompt)

    score, score_suggestions = score_prompt(prompt)

    statistics = stats_engine.calculate(prompt)

    # ------------------------------------------

    st.success("Analysis Completed Successfully")

    st.divider()

    # ------------------------------------------
    # Top Metrics
    # ------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Overall Score",
        f"{score}/100"
    )

    c2.metric(
        "Prompt Category",
        category.category
    )

    c3.metric(
        "Confidence",
        f"{int(category.confidence*100)}%"
    )

    c4.metric(
        "Complexity",
        analysis.complexity
    )

    st.progress(
        score / 100
    )

    st.divider()

    # ------------------------------------------
    # Detailed Scores
    # ------------------------------------------

    st.subheader("Quality Breakdown")

    left, right = st.columns(2)

    with left:

        st.metric(
            "Clarity",
            analysis.clarity_score
        )

        st.progress(
            analysis.clarity_score / 20
        )

        st.metric(
            "Context",
            analysis.context_score
        )

        st.progress(
            analysis.context_score / 20
        )

        st.metric(
            "Specificity",
            analysis.specificity_score
        )

        st.progress(
            analysis.specificity_score / 15
        )

    with right:

        st.metric(
            "Persona",
            analysis.persona_score
        )

        st.progress(
            analysis.persona_score / 15
        )

        st.metric(
            "Constraints",
            analysis.constraints_score
        )

        st.progress(
            analysis.constraints_score / 15
        )

        st.metric(
            "Output Format",
            analysis.format_score
        )

        st.progress(
            analysis.format_score / 15
        )

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

    if analysis.overall_score >= 90:

        st.success(
            "Excellent prompt. Ready for production use."
        )

    elif analysis.overall_score >= 75:

        st.success(
            "Very good prompt. Minor improvements recommended."
        )

    elif analysis.overall_score >= 55:

        st.warning(
            "Average prompt. Consider adding more context and constraints."
        )

    else:

        st.error(
            "Weak prompt. It should be rewritten before using with an LLM."
        )

# ----------------------------------------------------
# Footer
# ----------------------------------------------------

st.markdown("---")

st.caption(
    "PromptForge AI • Phase 2 • Prompt Analyzer"
)