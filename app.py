import streamlit as st
from dotenv import load_dotenv
from main import run_pipeline
from core.rag_engine import ask_question

load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎥",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("🎥 AI Video Assistant")
st.markdown("### Upload videos or YouTube links and chat with your content")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Settings")

language = st.sidebar.selectbox(
    "Select Language",
    ["english", "hinglish"]
)

# ---------------- INPUT ----------------
source = st.text_input("📌 Enter YouTube URL or Local File Path")

# ---------------- PROCESS BUTTON ----------------
if st.button("🚀 Process Video"):
    if not source:
        st.warning("Please enter a valid source")
        st.stop()

    with st.spinner("Processing video..."):
        # Run pipeline and save the entire result into session state
        result = run_pipeline(source, language)
        st.session_state["result"] = result
        st.session_state["rag_chain"] = result["rag_chain"]
        st.success("Processing Complete ✅")

# ---------------- DISPLAY RESULTS ----------------
# This checks if the video has been processed and keeps it visible
if "result" in st.session_state:
    result = st.session_state["result"]

    st.markdown("---")
    st.subheader("📌 Generated Title")
    st.info(result.get("title", "No Title Generated"))

    st.subheader("📋 Summary")
    st.write(result.get("summary", "No Summary Available"))

    st.subheader("✅ Action Items")
    st.write(result.get("action_items", "None"))

    st.subheader("🔑 Key Decisions")
    st.write(result.get("key_decisions", "None"))

    st.subheader("❓ Open Questions")
    st.write(result.get("open_questions", "None"))

    with st.expander("📝 View Full Transcript"):
        st.write(result.get("transcript", "No transcript available."))

# ---------------- CHAT SECTION ----------------
if "rag_chain" in st.session_state:
    st.markdown("---")
    st.subheader("💬 Chat With Your Video")

    # We use a form here so pressing enter or clicking submit
    # bundles the question submission perfectly without broken states.
    with st.form(key="chat_form", clear_on_submit=False):
        user_question = st.text_input("Ask a question about the video")
        submit_button = st.form_submit_button(label="🤖 Get Answer")

    if submit_button:
        if user_question.strip():
            with st.spinner("Thinking..."):
                answer = ask_question(
                    st.session_state["rag_chain"],
                    user_question
                )
                st.write("### 🤖 Answer:")
                st.info(answer)
        else:
            st.warning("Please enter a question first!")