import streamlit as st
import requests

st.set_page_config(page_title="PaperForge", page_icon="📄")

st.title("📄 PaperForge")

project_description = st.text_area(
    "🧠 Project Overview",
    height=200
)

paper_format = st.selectbox("📑 Format", ["IEEE"])
pages = st.slider("📄 Pages", 4, 20, 8)

if st.button("⚡ Forge Research Paper"):

    with st.status("🚀 Processing request...", expanded=True) as status:

        # 1️⃣ Validation
        status.write("✅ Validating input...")
        if len(project_description.strip()) < 30:
            st.error("Project overview too short")
            status.update(label="❌ Validation failed", state="error")
            st.stop()

        # 2️⃣ Prompt generation
        status.write("🧠 Generating academic prompt...")

        payload = {
            "overview": project_description,
            "format": paper_format,
            "npages": pages
        }

        # 3️⃣ LLM response + DOC generation
        status.write("🤖 Calling LLM and generating paper...")
        response = requests.post(
            "http://127.0.0.1:8000/generate-docs",
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            status.update(label="❌ Backend error", state="error")
            st.stop()

        data = response.json()
        output_file = data.get("file")

        status.write("📄 Finalizing DOCX...")
        status.update(label="✅ Paper generated successfully!", state="complete")

    # 🔽 DOWNLOAD
    with open(output_file, "rb") as f:
        st.download_button(
            "📥 Download Research Paper",
            f,
            file_name=output_file,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
