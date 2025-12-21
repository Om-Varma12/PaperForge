# front/main.py

import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="PaperForge", page_icon="📄")

st.title("📄 PaperForge")

# Test download button for existing file
st.sidebar.title("🔧 Test Downloads")
if st.sidebar.button("📥 Download Existing Paper"):
    try:
        # Get path to back/output.docx
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        file_path = os.path.join(parent_dir, "back", "output.docx")
        
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.sidebar.download_button(
                    "📄 Download output.docx",
                    f,
                    file_name="output.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    key="sidebar_download"
                )
        else:
            st.sidebar.error("❌ File not found at back/output.docx")
    except Exception as e:
        st.sidebar.error(f"❌ Error: {str(e)}")

project_description = st.text_area("🧠 Project Overview", height=200)
paper_format = st.selectbox("📑 Format", ["IEEE"])
pages = st.slider("📄 Pages", 4, 20, 8)


def process_sse_stream(url, payload):
    """Process Server-Sent Events stream from FastAPI"""
    
    # Create separate containers for each spinner
    validation_container = st.empty()
    prompt_container = st.empty()
    llm_container = st.empty()
    doc_container = st.empty()
    
    spinners = {
        "validation": {
            "container": validation_container,
            "message": "🔍 Validating inputs...",
            "spinner": None
        },
        "prompt_generation": {
            "container": prompt_container,
            "message": "🧠 Generating academic prompt...",
            "spinner": None
        },
        "llm_response": {
            "container": llm_container,
            "message": "🤖 Getting response from LLM...",
            "spinner": None
        },
        "document_generation": {
            "container": doc_container,
            "message": "📄 Generating IEEE formatted document...",
            "spinner": None
        }
    }
    
    output_file = None
    
    try:
        response = requests.post(
            url, 
            json=payload, 
            stream=True, 
            timeout=180,
            headers={'Accept': 'text/event-stream'}
        )
        
        # Process the stream line by line
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                
                # SSE format: "data: {json}"
                if line.startswith('data: '):
                    data_str = line[6:]  # Remove "data: " prefix
                    
                    try:
                        data = json.loads(data_str)
                        stage = data.get("stage")
                        status = data.get("status")
                        event_data = data.get("data", {})
                        
                        # Handle each stage
                        if status == "started":
                            if stage in spinners:
                                spinner_info = spinners[stage]
                                spinner_info["spinner"] = spinner_info["container"].status(
                                    spinner_info["message"], 
                                    expanded=True,
                                    state="running"
                                )
                        
                        elif status == "completed":
                            if stage in spinners and spinners[stage]["spinner"]:
                                spinners[stage]["spinner"].update(
                                    label=f"✅ {spinners[stage]['message'].split('...')[0]} completed",
                                    state="complete"
                                )
                        
                        elif status == "error":
                            st.error(f"❌ Error: {event_data.get('message', 'Unknown error')}")
                            return None
                        
                        elif status == "success":
                            output_file = event_data.get("file")
                            st.success("✅ Research paper generated successfully!")
                            return output_file
                    
                    except json.JSONDecodeError:
                        continue
        
        return output_file
        
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. Please try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Could not connect to backend. Ensure FastAPI server is running.")
        return None
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        return None


if st.button("⚡ Forge Research Paper"):
    
    # Quick validation before sending request
    if len(project_description.strip()) < 30:
        st.error("Project overview must be at least 30 characters.")
        st.stop()
    
    payload = {
        "overview": project_description,
        "format": paper_format,
        "npages": pages
    }
    
    # Process the streaming response
    output_file = process_sse_stream(
        "http://127.0.0.1:8000/generate-docs-stream",
        payload
    )
    
    # Download button if successful
    if output_file:
        try:
            # Get the parent directory (where both front/ and back/ are located)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            
            # Construct path to back/output.docx
            file_path = os.path.join(parent_dir, "back", output_file)
            
            # Check if file exists
            if not os.path.exists(file_path):
                st.error(f"❌ Generated file not found at: {file_path}")
                st.stop()
            
            with open(file_path, "rb") as f:
                file_bytes = f.read()
                st.download_button(
                    "📥 Download Research Paper",
                    file_bytes,
                    file_name=os.path.basename(output_file),
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")