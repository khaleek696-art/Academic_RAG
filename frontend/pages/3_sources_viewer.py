import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Sources Viewer", page_icon="📖", layout="wide")
st.title("📖 Sources & Chunks Inspector")

doc_id = st.number_input("Enter Document ID to inspect chunks", min_value=1, value=1, step=1)

if st.button("Inspect Chunks"):
    try:
        res = requests.get(f"{BACKEND_URL}/documents/{doc_id}/chunks")
        if res.status_code == 200:
            chunks = res.json()
            if chunks:
                st.success(f"Found {len(chunks)} chunks for Document ID {doc_id}")
                for chunk in chunks:
                    with st.expander(f"Chunk ID #{chunk['id']} — Page {chunk['page']}"):
                        st.write(chunk["text"])
                        st.caption(f"Ref: {chunk.get('embedding_ref')}")
            else:
                st.warning("No chunks found for this Document ID.")
        else:
            st.error("Document not found.")
    except Exception as e:
        st.error(f"Error fetching chunks: {str(e)}")
