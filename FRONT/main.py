import streamlit as st
import requests

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="PaperForge",
    page_icon="📄",
    layout="centered"
)

# -------------------- Load CSS --------------------
with open("./assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------- Header --------------------
st.markdown(
    """
    <div style="text-align:center; margin-bottom:3rem;">
        <div class="paperforge-title">PaperForge</div>
        <div class="paperforge-subtitle">
            Forge academic research papers in minutes, not weeks.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------- Main Card --------------------
# st.markdown('<div class="card">', unsafe_allow_html=True)

project_description = st.text_area(
    "🧠 Project Overview",
    placeholder="Describe your project in simple language...\n\nExample:\nThis project uses machine learning to detect phishing websites by analyzing URLs, SSL certificates, and domain metadata.",
    height=200
)

col1, col2 = st.columns(2)

with col1:
    paper_format = st.selectbox(
        "📑 Publication Format",
        ["IEEE", "Springer", "ACM", "Elsevier"]
    )

with col2:
    pages = st.slider(
        "📄 Target Pages",
        min_value=4,
        max_value=20,
        value=8
    )

sections = st.multiselect(
    "🧩 Paper Sections",
    [
        "Abstract",
        "Introduction",
        "Literature Review",
        "Problem Statement",
        "Methodology",
        "System Architecture",
        "Experimental Results",
        "Discussion",
        "Conclusion",
        "Future Work",
        "References"
    ],
    default=[
        "Abstract",
        "Introduction",
        "Literature Review",
        "Methodology",
        "Experimental Results",
        "Conclusion",
        "References"
    ]
)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------- Generate --------------------
generate = st.button("⚡ Forge Research Paper")

if generate:
    payload = {
        "overview": project_description,
        "format": paper_format,
        "npages": pages,
        "section": sections
    }

    with st.spinner("Sending data to backend..."):
        try:    
            response = requests.post(
                "http://localhost:8000/generate-docs",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    st.success("✅ Backend connected successfully!")
                else:
                    st.error("❌ Backend returned an error")
                # st.json(data)

            else:
                try:
                    error_data = response.json()

                    # ✅ FASTAPI VALIDATION ERRORS
                    if response.status_code == 422 and "detail" in error_data:
                        st.error("❌ Backend validation failed")

                        for err in error_data["detail"]:
                            field = err["loc"][-1]
                            message = err["msg"]
                            st.warning(f"⚠️ {field}: {message}")

                    else:
                        st.error("❌ Backend error")
                        st.code(error_data)

                except Exception:
                    st.error("❌ Backend error")
                    st.code(response.text)

                    
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Could not connect to backend: {e}")