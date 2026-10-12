import streamlit as st
import difflib

from utils.prompt_stats import PromptStats
from models.classifier import PromptClassifier
from utils.helper import load_custom_css, render_sidebar_branding, render_page_header, render_footer


st.set_page_config(
    page_title="Prompt Comparison | PromptForge AI",
    page_icon="⚖️",
    layout="wide"
)

load_custom_css()
render_sidebar_branding()

stats_engine = PromptStats()
classifier = PromptClassifier()

# --------------------------------------------------
# Header
# --------------------------------------------------

render_page_header(
    title="Prompt Comparison",
    subtitle="Compare original vs. optimized prompts side-by-side with visual diffs and token efficiency analysis.",
    icon="⚖️",
    badge="SIDE-BY-SIDE DIFF"
)

st.divider()

# --------------------------------------------------
# Inputs
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    original_prompt = st.text_area(
        "Original Prompt",
        height=300,
        placeholder="Paste your original prompt..."
    )

with col2:

    optimized_prompt = st.text_area(
        "Optimized Prompt",
        height=300,
        placeholder="Paste your optimized prompt..."
    )

compare = st.button(
    "Compare Prompts",
    use_container_width=True
)

# --------------------------------------------------
# Comparison
# --------------------------------------------------

if compare:

    if not original_prompt.strip():

        st.warning("Please enter the original prompt.")

        st.stop()

    if not optimized_prompt.strip():

        st.warning("Please enter the optimized prompt.")

        st.stop()

    original_stats = stats_engine.calculate(original_prompt)

    optimized_stats = stats_engine.calculate(optimized_prompt)

    original_category = classifier.classify(original_prompt)

    optimized_category = classifier.classify(optimized_prompt)

    st.success("Comparison Generated")

    st.divider()

    # --------------------------------------------
    # Metrics
    # --------------------------------------------

    st.subheader("📊 Statistics Comparison")

    metrics = [

        ("Words",
         original_stats.word_count,
         optimized_stats.word_count),

        ("Characters",
         original_stats.character_count,
         optimized_stats.character_count),

        ("Estimated Tokens",
         original_stats.estimated_tokens,
         optimized_stats.estimated_tokens),

        ("Reading Time",
         original_stats.estimated_reading_time,
         optimized_stats.estimated_reading_time),

        ("Complexity",
         original_stats.complexity,
         optimized_stats.complexity),

        ("Readability",
         original_stats.readability,
         optimized_stats.readability)

    ]

    for metric in metrics:

        c1, c2, c3 = st.columns([2, 2, 2])

        c1.markdown(f"**{metric[0]}**")

        c2.info(metric[1])

        c3.success(metric[2])

    st.divider()

    # --------------------------------------------
    # Category Comparison
    # --------------------------------------------

    st.subheader("🏷 Prompt Category")

    c1, c2 = st.columns(2)

    c1.metric(
        "Original",
        original_category.category
    )

    c2.metric(
        "Optimized",
        optimized_category.category
    )

    st.divider()

    # --------------------------------------------
    # Improvements
    # --------------------------------------------

    st.subheader("✨ Improvements")

    improvements = []

    if optimized_stats.word_count > original_stats.word_count:
        improvements.append(
            "Added more context and descriptive information."
        )

    if optimized_stats.estimated_tokens > original_stats.estimated_tokens:
        improvements.append(
            "Prompt contains richer instructions."
        )

    if optimized_stats.complexity != original_stats.complexity:
        improvements.append(
            "Prompt complexity has been improved."
        )

    if optimized_stats.readability == "Medium":
        improvements.append(
            "Improved readability."
        )

    if original_category.category != optimized_category.category:
        improvements.append(
            "Prompt category became more specific."
        )

    keywords = [
        "markdown",
        "json",
        "table",
        "bullet",
        "act as",
        "must",
        "only",
        "do not"
    ]

    for word in keywords:

        if word in optimized_prompt.lower() and word not in original_prompt.lower():

            improvements.append(
                f"Added '{word}' instruction."
            )

    if improvements:

        for item in improvements:

            st.success(item)

    else:

        st.info("No major improvements detected.")

    st.divider()

    # --------------------------------------------
    # Text Difference
    # --------------------------------------------

    st.subheader("📝 Line-by-Line Difference")

    diff = difflib.ndiff(
        original_prompt.splitlines(),
        optimized_prompt.splitlines()
    )

    for line in diff:

        if line.startswith("+"):

            st.success(line)

        elif line.startswith("-"):

            st.error(line)

        elif line.startswith("?"):

            continue

        else:

            st.write(line)

    st.divider()

    # --------------------------------------------
    # Side-by-Side Preview
    # --------------------------------------------

    st.subheader("📄 Prompt Preview")

    left, right = st.columns(2)

    with left:

        st.markdown("### Original")

        st.code(
            original_prompt,
            language="text"
        )

    with right:

        st.markdown("### Optimized")

        st.code(
            optimized_prompt,
            language="text"
        )

    st.divider()

    # --------------------------------------------
    # Final Verdict
    # --------------------------------------------

    st.subheader("🎯 Final Verdict")

    score = 0

    if optimized_stats.word_count > original_stats.word_count:
        score += 1

    if optimized_stats.estimated_tokens > original_stats.estimated_tokens:
        score += 1

    if optimized_stats.complexity != original_stats.complexity:
        score += 1

    if len(improvements) >= 3:
        score += 1

    if score >= 4:

        st.success(
            "Excellent optimization. The prompt is significantly improved."
        )

    elif score >= 2:

        st.info(
            "Good optimization. The prompt is better than the original."
        )

    else:

        st.warning(
            "Only minor improvements were detected."
        )

# --------------------------------------------------
# Footer
# --------------------------------------------------

render_footer()