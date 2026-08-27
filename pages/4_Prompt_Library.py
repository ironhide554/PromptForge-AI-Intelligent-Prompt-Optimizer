import streamlit as st
from utils.templates import PromptTemplates

st.set_page_config(
    page_title="Prompt Library",
    page_icon="📚",
    layout="wide"
)

template_manager = PromptTemplates()

st.title("📚 Prompt Library")
st.write("Browse and preview built-in prompt templates.")

# -------------------------------
# Search
# -------------------------------

search = st.text_input(
    "🔍 Search Templates",
    placeholder="Search by template name..."
)

categories = ["All"] + template_manager.get_categories()

selected_category = st.selectbox(
    "Category",
    categories
)

st.divider()

# -------------------------------
# Display Templates
# -------------------------------

templates = template_manager.get_all_templates()

filtered = []

for template in templates:

    if selected_category != "All":

        if template.name != selected_category:
            continue

    if search:

        text = (
            template.name +
            template.category +
            template.description
        ).lower()

        if search.lower() not in text:
            continue

    filtered.append(template)

if not filtered:

    st.warning("No templates found.")

else:

    for template in filtered:

        with st.expander(f"📄 {template.name}"):

            st.markdown(f"**Category:** {template.category}")

            st.markdown(f"**Description:** {template.description}")

            st.markdown("### Prompt Template")

            st.code(
                template.template,
                language="text"
            )

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📄 Download TXT",
                    data=template.template,
                    file_name=f"{template.name}.txt",
                    mime="text/plain",
                    key=f"txt_{template.name}"
                )
            with col2:
                try:
                    from utils.pdf_generator import generate_pdf
                    pdf_bytes = generate_pdf(template.template)
                    st.download_button(
                        "📑 Download PDF",
                        data=pdf_bytes,
                        file_name=f"{template.name}.pdf",
                        mime="application/pdf",
                        key=f"pdf_{template.name}"
                    )
                except Exception:
                    st.error("PDF Error")

st.divider()

st.caption("PromptForge AI • Prompt Library")