import streamlit as st

st.set_page_config(
    page_title="Academic QA RAG System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📚 Academic Question Answering System Using RAG")
st.markdown("""
Welcome to your **Academic AI Teaching Assistant**!

This system lets you:
1. 📤 **Upload Study Materials**: Organize PDFs (textbooks, notes, slides) by Subject.
2. 💬 **Ask Exam & Concept Questions**: Get precise answers grounded **strictly** in your uploaded materials.
3. 📖 **Inspect Source Citations**: Verify exact document names and page numbers.
4. 📊 **Give Feedback**: Help improve the system with helpfulness logging.

---
### 👈 Use the sidebar navigation on the left to get started!
- **1. Upload & Subjects**: Manage subjects and upload PDFs.
- **2. Ask Questions**: Ask Q&A with custom answer modes.
- **3. Sources Viewer**: Inspect extracted text chunks per page.
- **4. History & Feedback**: View past chats & submit feedback.
""")

st.info("💡 **Backend Status**: Connected to FastAPI + SQLite + Qdrant Local Vector Engine.")
