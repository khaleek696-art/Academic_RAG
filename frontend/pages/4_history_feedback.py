import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="History & Feedback", page_icon="📊", layout="wide")
st.title("📊 History & Feedback Logging")

st.subheader("👍 / 👎 Submit Feedback on Answer")

msg_id = st.number_input("Message ID (from Q&A output)", min_value=1, value=1, step=1)
helpful = st.radio("Was the answer helpful?", [True, False], format_func=lambda x: "👍 Yes, helpful" if x else "👎 No, unhelpful")
comment = st.text_area("Optional Feedback Comment", placeholder="e.g. Citation was accurate and clear.")

if st.button("Submit Feedback"):
    try:
        payload = {
            "message_id": msg_id,
            "helpful": helpful,
            "comment": comment
        }
        res = requests.post(f"{BACKEND_URL}/feedback", json=payload)
        if res.status_code == 201:
            st.success("✅ Thank you! Feedback recorded in SQLite database.")
        else:
            st.error(res.json().get("detail", "Error recording feedback"))
    except Exception as e:
        st.error(f"Error submitting feedback: {str(e)}")
