import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Ask Questions", page_icon="💬", layout="wide")
st.title("💬 Academic Question Answering")

# Load Subjects
subjects_list = []
try:
    res = requests.get(f"{BACKEND_URL}/subjects")
    if res.status_code == 200:
        subjects_list = res.json()
except Exception:
    pass

col1, col2 = st.columns([2, 1])

with col1:
    subject_options = ["All Subjects"] + [f"{s['name']} (ID: {s['id']})" for s in subjects_list]
    selected_sub = st.selectbox("Filter by Subject", subject_options)

    subject_id = None
    if selected_sub != "All Subjects":
        subject_id = int(selected_sub.split("ID: ")[1].replace(")", ""))

with col2:
    mode = st.radio("Answer Style Mode", ["short", "detailed", "exam"], index=1)

question = st.text_area("Ask a question from your uploaded study materials:", placeholder="e.g. What is process synchronization in Operating Systems?", height=100)

if st.button("🚀 Get Cited Answer", type="primary"):
    if question.strip():
        with st.spinner("Searching Qdrant + BM25, reranking, and generating cited answer..."):
            try:
                payload = {
                    "question": question,
                    "subject_id": subject_id,
                    "mode": mode
                }
                res = requests.post(f"{BACKEND_URL}/ask", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.markdown("### 📝 Answer:")
                    if data.get("refused"):
                        st.warning(data["answer"])
                    else:
                        st.markdown(data["answer"])
                        st.caption(f"🎯 Confidence Score: {data['confidence']}")

                        st.markdown("---")
                        st.markdown("### 📄 **Source Citations:**")
                        for c in data.get("citations", []):
                            st.info(f"• **Document**: `{c['document_name']}` | **Page**: `{c['page_number']}`\n\n*Snippet*: _{c.get('snippet', '')}_")
                else:
                    st.error("Error generating answer.")
            except Exception as e:
                st.error(f"Failed to connect to backend: {str(e)}")
    else:
        st.warning("Please type a question.")
