import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Upload & Subjects", page_icon="📤", layout="wide")
st.title("📤 Manage Subjects & Upload PDFs")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("➕ Create New Subject")
    new_subject_name = st.text_input("Subject Name", placeholder="e.g. Operating Systems")
    if st.button("Create Subject"):
        if new_subject_name:
            try:
                res = requests.post(f"{BACKEND_URL}/subjects", json={"name": new_subject_name})
                if res.status_code == 201:
                    st.success(f"✅ Subject '{new_subject_name}' created successfully!")
                else:
                    st.error(res.json().get("detail", "Error creating subject"))
            except Exception as e:
                st.error(f"Failed to connect to backend: {str(e)}")
        else:
            st.warning("Please enter a subject name.")

with col2:
    st.subheader("📚 Available Subjects")
    try:
        res = requests.get(f"{BACKEND_URL}/subjects")
        if res.status_code == 200:
            subjects = res.json()
            if subjects:
                for s in subjects:
                    st.markdown(f"- **ID {s['id']}**: {s['name']}")
            else:
                st.info("No subjects created yet.")
        else:
            st.error("Error fetching subjects.")
    except Exception as e:
        st.error(f"Backend offline: {str(e)}")

st.markdown("---")
st.subheader("📄 Upload PDF Study Material")

# Fetch subjects for dropdown
subjects_list = []
try:
    res = requests.get(f"{BACKEND_URL}/subjects")
    if res.status_code == 200:
        subjects_list = res.json()
except Exception:
    pass

if not subjects_list:
    st.warning("⚠️ Please create at least one Subject above before uploading PDFs.")
else:
    subject_map = {f"{s['name']} (ID: {s['id']})": s["id"] for s in subjects_list}
    selected_subject_str = st.selectbox("Select Subject", list(subject_map.keys()))
    selected_subject_id = subject_map[selected_subject_str]

    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if st.button("Upload & Index into Qdrant"):
        if uploaded_file is not None:
            with st.spinner("Indexing PDF page-by-page into Qdrant & BM25..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                    data = {"subject_id": selected_subject_id}
                    response = requests.post(f"{BACKEND_URL}/documents", files=files, data=data)
                    if response.status_code == 201:
                        doc = response.json()
                        st.success(f"🎉 Document '{doc['filename']}' indexed! ({doc['pages']} pages, {doc['chunks_count']} chunks)")
                    else:
                        st.error(response.json().get("detail", "Error uploading document"))
                except Exception as e:
                    st.error(f"Upload failed: {str(e)}")
        else:
            st.warning("Please select a PDF file first.")
