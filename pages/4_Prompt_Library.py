import streamlit as st
from utils.templates import PromptTemplates

st.set_page_config(
    page_title="Prompt Library",
    page_icon="📚",
    layout="wide"
)

template_manager = PromptTemplates()

st.title("📚 Prompt Library & Marketplace")
st.write("Browse built-in prompt templates or discover new ones from the community.")

tab_local, tab_market = st.tabs(["🏡 Local Library", "🌐 Marketplace"])

with tab_local:
    st.subheader("Your Prompt Templates")
    
    search = st.text_input("🔍 Search Local Templates", placeholder="Search by name...")
    categories = ["All"] + template_manager.get_categories()
    selected_category = st.selectbox("Category", categories, key="local_cat")
    
    st.divider()
    
    templates = template_manager.get_all_templates()
    filtered = []
    
    for template in templates:
        if selected_category != "All" and template.name != selected_category:
            continue
        if search:
            text = (template.name + template.category + template.description).lower()
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
                st.code(template.template, language="text")
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

with tab_market:
    st.subheader("Community Marketplace")
    st.info("Discover and download prompt templates shared by the community.")
    
    market_search = st.text_input("🔍 Search Marketplace", placeholder="Search community templates...")
    
    # Mock Marketplace Data
    mock_market_templates = [
        {"name": "Python Fast API Expert", "author": "@devguru", "downloads": 1204, "rating": "⭐⭐⭐⭐⭐"},
        {"name": "Creative Story Writer", "author": "@fiction_ai", "downloads": 842, "rating": "⭐⭐⭐⭐"},
        {"name": "React Component Generator", "author": "@frontend_wiz", "downloads": 3051, "rating": "⭐⭐⭐⭐⭐"},
        {"name": "Cold Email Outreach", "author": "@sales_pro", "downloads": 432, "rating": "⭐⭐⭐"},
    ]
    
    for t in mock_market_templates:
        if market_search.lower() in t["name"].lower() or market_search.lower() in t["author"].lower():
            with st.container():
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"**{t['name']}** by {t['author']}")
                c2.markdown(f"📥 {t['downloads']} | {t['rating']}")
                if c3.button("⬇ Get Template", key=f"get_{t['name']}"):
                    st.success(f"Successfully downloaded '{t['name']}' to your local library! (Simulated)")
                st.divider()

st.divider()
st.caption("PromptForge AI • Prompt Library & Marketplace")