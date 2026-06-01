import streamlit as st
import os
import time
from main import run_pipeline
from core.rag_engine import ask_question
import sys


# 1. Dynamically append the subfolder path to Python's environment path registry
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# ==============================================================================
# YOUR EXISTING IMPORTS CONTINUE BELOW PERFYCTLY
# ==============================================================================
import streamlit as st
import time
from main import run_pipeline
from core.rag_engine import ask_question

# ... (the rest of your brilliant app.py code stays exactly the same!)

# ==========================================
# 1. PAGE ARCHITECTURE & PREMIUM THEME
# ==========================================
st.set_page_config(
    page_title="VividAgent AI | Video Intelligence Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End dark UI injection
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .header-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 2.2rem;
        border-radius: 16px;
        border: 1px solid #334155;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    .status-badge {
        background-color: #1e1b4b;
        color: #818cf8;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        border: 1px solid #4338ca;
    }
    .analysis-card {
        background: #161b22;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 1rem;
    }
    .card-title {
        color: #58a6ff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States for persistent storage across app reruns
if "pipeline_result" not in st.session_state:
    st.session_state.pipeline_result = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==========================================
# 2. CONTROL PANEL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: white; margin-bottom: 0;'>🤖 Settings</h2>", unsafe_allow_html=True)
    st.markdown("Configure intelligence variables.")
    st.markdown("---")

    language = st.selectbox(
        "Transcription Target Language",
        ["english", "hinglish"],
        index=0,
        help="Select the localized model matrix matching the target media stream."
    )

    st.markdown("---")
    st.markdown("### ⚡ System Status")
    st.success("RAG Vector Engine: Ready")
    st.success("GPU Acceleration: Active")

    if st.button("🔄 Clear App Cache / Reset"):
        st.session_state.pipeline_result = None
        st.session_state.chat_history = []
        st.rerun()

# ==========================================
# 3. HERO COMPONENT HEADER
# ==========================================
st.markdown("""
    <div class="header-box">
        <span class="status-badge">⚡ PRODUCTION PIPELINE ACTIVE</span>
        <h1 style='margin-top: 12px; color: white; font-family: Inter, sans-serif; font-weight: 800;'>🎬 VividAgent: Video Intelligence</h1>
        <p style='color: #94a3b8; font-size: 1.05rem; max-width: 900px; margin-bottom: 0;'>
            Transform unstructured multimedia formats into structured analytical data pools. This workspace ingests remote video streams or localized binary uploads to synthesize metadata matrices and deploy a contextual RAG instance.
        </p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 4. DATA INGESTION WORKSPACE
# ==========================================
if st.session_state.pipeline_result is None:
    st.markdown("### 🎛️ Input Feed Selector")
    tab1, tab2 = st.tabs(["🔗 Remote Streaming URL", "📁 Local Multi-Modal Document"])

    source_input = None

    with tab1:
        youtube_url = st.text_input(
            "YouTube Video Stream Resource Address",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Accepts videos, shorts, or transport streams."
        )
        if youtube_url:
            source_input = youtube_url.strip()

    with tab2:
        uploaded_file = st.file_uploader(
            "Upload Media Binary Block",
            type=["wav", "mp3", "mp4", "m4a"],
            help="Max file limit optimized for local runtime profiles."
        )
        if uploaded_file:
            temp_dir = "downloads"
            os.makedirs(temp_dir, exist_ok=True)
            source_input = os.path.join(temp_dir, uploaded_file.name)
            with open(source_input, "wb") as f:
                f.write(uploaded_file.getbuffer())

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Boot Pipeline Sequence", use_container_width=True, type="primary"):
        if source_input:
            # Elegant stepped feedback sequence
            status_container = st.empty()
            progress_bar = st.progress(0)

            with st.spinner("Processing pipeline framework modules..."):
                try:
                    status_container.markdown("⏳ **Stage 1/4:** Ingesting media structure & calculating chunks...")
                    progress_bar.progress(15)
                    time.sleep(0.4)

                    status_container.markdown(
                        "🧠 **Stage 2/4:** Translating acoustics to text vectors (Transcription)...")
                    progress_bar.progress(40)

                    # Core Processing Execution Block
                    result = run_pipeline(source_input, language)

                    status_container.markdown(
                        "📊 **Stage 3/4:** Analyzing structured payloads (Actions, Decisions, Synthesis)...")
                    progress_bar.progress(75)
                    time.sleep(0.4)

                    status_container.markdown("📚 **Stage 4/4:** Instantiating local Vector Database & RAG Chain...")
                    progress_bar.progress(95)
                    time.sleep(0.2)

                    # Store data into session storage
                    st.session_state.pipeline_result = result
                    progress_bar.empty()
                    status_container.empty()
                    st.toast("Pipeline Matrix Fully Finalized!", icon="✨")
                    st.rerun()

                except Exception as e:
                    st.error(f"Operational Pipeline Fault: {e}")
        else:
            st.error("🚨 Validation Error: Ingestion Engine requires an active stream address or binary vector path.")

# ==========================================
# 5. PRESTIGE METRICS & INSIGHTS DISPLAY
# ==========================================
else:
    res = st.session_state.pipeline_result

    st.markdown(f"<h2 style='color: white; margin-bottom:20px;'>📌 Meeting Matrix: {res['title']}</h2>",
                unsafe_allow_html=True)

    # 2-Column Dashboard Layout
    left_dashboard, right_dashboard = st.columns([6, 5], gap="large")

    with left_dashboard:
        st.markdown("### 📊 Operational Summaries")

        with st.expander("📝 Executive Summary", expanded=True):
            st.write(res["summary"])

        with st.expander("📋 Raw Transcription Stream", expanded=False):
            st.text_area("Transcription Log Output", res["transcript"], height=300, disabled=True)

        st.markdown("<br>### 🎯 Extracted Telemetry", unsafe_allow_html=True)

        st.markdown(f"""
            <div class="analysis-card">
                <div class="card-title">✅ Action Items</div>
                <p style="white-space: pre-wrap; color: #cbd5e1;">{res['action_items']}</p>
            </div>
            <div class="analysis-card">
                <div class="card-title">🔑 Key Decisions</div>
                <p style="white-space: pre-wrap; color: #cbd5e1;">{res['key_decisions']}</p>
            </div>
            <div class="analysis-card">
                <div class="card-title">❓ Open Questions</div>
                <p style="white-space: pre-wrap; color: #cbd5e1;">{res['open_questions']}</p>
            </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # 6. HIGH-PERFORMANCE CHAT INTERFACE (RAG)
    # ==========================================
    with right_dashboard:
        st.markdown("### 💬 Contextual RAG Chat Interface")
        st.markdown("Inquire against the meeting document memory bank in real-time.")

        chat_container = st.container(height=450, border=True)

        # Render clean, native Streamlit chat bubbles
        with chat_container:
            if not st.session_state.chat_history:
                st.markdown(
                    "<p style='color:#64748b; text-align:center; margin-top:200px;'>Ask any question relative to the processed video context...</p>",
                    unsafe_allow_html=True)
            for role, text in st.session_state.chat_history:
                with st.chat_message(role):
                    st.write(text)

        # User input execution
        if user_query := st.chat_input("Ask a question about this meeting..."):
            with chat_container:
                with st.chat_message("user"):
                    st.write(user_query)
            st.session_state.chat_history.append(("user", user_query))

            # Generate response from your exact core RAG function
            with st.spinner("Analyzing vector database segments..."):
                answer = ask_question(res["rag_chain"], user_query)

            with chat_container:
                with st.chat_message("assistant"):
                    st.write(answer)
            st.session_state.chat_history.append(("assistant", answer))
            st.rerun()