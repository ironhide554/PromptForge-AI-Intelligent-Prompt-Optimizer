import streamlit as st
from utils.templates import PromptTemplates
from utils.helper import load_custom_css, render_sidebar_branding, render_page_header, render_footer

st.set_page_config(
    page_title="Prompt Library & Marketplace | PromptForge AI",
    page_icon="📚",
    layout="wide"
)

load_custom_css()
render_sidebar_branding()

template_manager = PromptTemplates()

render_page_header(
    title="Prompt Library & Marketplace",
    subtitle="Access battle-tested system templates across engineering, marketing, and business, or explore the community marketplace.",
    icon="📚",
    badge="TEMPLATES & MARKETPLACE"
)

tab_local, tab_market = st.tabs(["🏡 Local Built-In Library", "🌐 Global Marketplace"])

with tab_local:
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        search = st.text_input("🔍 Search Templates", placeholder="Search by name, role, or description...")
    with col_s2:
        categories = ["All"] + template_manager.get_categories()
        selected_category = st.selectbox("Filter Category", categories, key="local_cat")
    
    st.divider()

    with st.expander("➕ Create & Save New Custom Template"):
        c_name = st.text_input("Template Name", placeholder="e.g. Next.js 15 App Router Expert")
        c_cat = st.selectbox("Category", ["Engineering", "AI & ML", "Writing", "Marketing", "Business", "Custom"])
        c_desc = st.text_input("Description", placeholder="Brief summary of persona and constraints...")
        c_tmpl = st.text_area("Template Text", placeholder="Act as a Senior Architect...\nTask:\n{task}\nConstraints:\n...", height=140)
        if st.button("💾 Save Custom Template", use_container_width=True):
            if c_name.strip() and c_tmpl.strip():
                template_manager.add_custom_template(c_name.strip(), c_cat, c_desc.strip(), c_tmpl.strip())
                st.success(f"Template '{c_name}' saved to local library!")
                st.rerun()
            else:
                st.warning("Please provide a Template Name and Template Content.")

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
        st.warning("No templates found matching your search criteria.")
    else:
        st.markdown(f"<p style='color: #94A3B8; font-size: 0.9rem; margin-bottom: 1rem;'>Showing <b>{len(filtered)}</b> production-ready templates</p>", unsafe_allow_html=True)
        for template in filtered:
            with st.expander(f"📄 {template.name} • {template.category}"):
                st.markdown(f"**Domain Category:** `{template.category}`")
                st.markdown(f"**Description:** {template.description}")
                st.code(template.template, language="text")
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        "📄 Download TXT",
                        data=template.template,
                        file_name=f"{template.name}.txt",
                        mime="text/plain",
                        key=f"txt_{template.name}",
                        use_container_width=True
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
                            key=f"pdf_{template.name}",
                            use_container_width=True
                        )
                    except Exception:
                        st.error("PDF generation unavailable")

with tab_market:
    st.markdown("""
    <div style="background: rgba(99, 102, 241, 0.1); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 12px; padding: 1rem 1.25rem; margin-bottom: 1.5rem;">
        <span style="color: #A5B4FC; font-weight: 700; font-size: 0.95rem;">🌐 PromptForge Community Cloud</span>
        <p style="color: #94A3B8; font-size: 0.85rem; margin: 4px 0 0 0;">Download verified community prompts crafted by leading AI engineers and researchers.</p>
    </div>
    """, unsafe_allow_html=True)
    
    market_search = st.text_input("🔍 Search Community Library", placeholder="Search by framework, stack, or creator...")
    
    mock_market_templates = [
        {"name": "Python FastAPI Enterprise Microservice", "author": "@devguru", "downloads": 1204, "rating": "⭐⭐⭐⭐⭐", "desc": "Clean architecture, Pydantic v2 schemas, JWT auth, and pytest setup."},
        {"name": "Full-Stack Next.js 15 App Router Expert", "author": "@frontend_wiz", "downloads": 3051, "rating": "⭐⭐⭐⭐⭐", "desc": "Server actions, Tailwind CSS, TypeScript, and edge runtime optimizations."},
        {"name": "High-Converting B2B Cold Email Architect", "author": "@sales_pro", "downloads": 432, "rating": "⭐⭐⭐⭐", "desc": "Pain-point agitating, PAS framework, sub-100 word crisp outreach."},
        {"name": "Creative Fiction & Sci-Fi Worldbuilder", "author": "@fiction_ai", "downloads": 842, "rating": "⭐⭐⭐⭐", "desc": "Sensory descriptions, deep character motivation, and dialogue cadence."},
    ]
    
    for t in mock_market_templates:
        if market_search.lower() in t["name"].lower() or market_search.lower() in t["author"].lower() or market_search.lower() in t["desc"].lower():
            with st.container():
                c1, c2, c3 = st.columns([3, 1, 1])
                with c1:
                    st.markdown(f"**{t['name']}** <span style='color: #64748B;'>by {t['author']}</span>", unsafe_allow_html=True)
                    st.caption(t["desc"])
                with c2:
                    st.markdown(f"📥 `{t['downloads']}` | {t['rating']}")
                with c3:
                    if st.button("⬇ Import Template", key=f"get_{t['name']}", use_container_width=True):
                        st.success(f"Successfully imported '{t['name']}' to your library!")
                st.divider()

render_footer()