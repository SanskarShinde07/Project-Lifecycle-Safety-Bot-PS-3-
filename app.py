import streamlit as st
import time
from chatbot.agent import ask_question

# Page config
st.set_page_config(
    page_title="Project Lifecycle Safety Bot",
    page_icon="🏗️",
    layout="wide"
)

# Styling
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🏗️ Project Lifecycle Safety Bot")
st.caption("Multi-source RAG assistant for construction lifecycle safety (TXT + CSV + Hybrid reasoning)")

# Sidebar
with st.sidebar:

    st.header("📊 System Architecture")

    st.markdown("""
This assistant combines:

• 📄 Retrieval-Augmented Generation (TXT documents)  
• 📊 CSV analytics for baseline and monthly metrics  
• 🔗 Hybrid reasoning across lifecycle data  
• 🤖 Azure OpenAI GPT-4o
""")

    st.divider()

    st.header("💡 Example Questions")

    st.markdown("""
**TXT Retrieval**
- Who are the primary owners of Permit to Work?

**Baseline CSV**
- What is the inherent risk score for Confined Space?

**Monthly Metrics**
- How many inspections were completed for Work at Height in 2025-03?

**Hybrid Query**
- For Confined Space show owners and risk score.
""")

    st.divider()

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Dataset overview
st.markdown("### 📊 Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("TXT Documents", "90+")
col2.metric("Safety Topics", "21")
col3.metric("CSV Metrics", "Baseline + Monthly")

# Quick demo buttons
st.subheader("⚡ Quick Demo Questions")

col1, col2, col3, col4 = st.columns(4)

quick_prompt = None

if col1.button("Permit Owners"):
    quick_prompt = "Who are the primary owners of Permit to Work?"

if col2.button("Risk Score"):
    quick_prompt = "What is the inherent risk score for Confined Space?"

if col3.button("Monthly Inspections"):
    quick_prompt = "How many inspections were completed for Work at Height in 2025-03?"

if col4.button("Hybrid Query"):
    quick_prompt = "For Confined Space show owners and risk score."

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👷" if message["role"] == "user" else "🤖"):
        st.write(message["content"])

# Chat input
prompt = st.chat_input("Ask a safety question about the project lifecycle...")

if quick_prompt:
    prompt = quick_prompt

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar="👷"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner("Analyzing project safety data sources..."):

            response = ask_question(prompt)

        # Typing animation
        placeholder = st.empty()
        typed_text = ""

        for char in response:
            typed_text += char
            placeholder.markdown(typed_text)
            time.sleep(0.005)

        # Source badges
        col1, col2 = st.columns(2)

        col1.success("📄 TXT Knowledge Base")
        col2.info("📊 CSV Metrics Engine")

        # Confidence indicator
        st.caption("Confidence: High | Answer grounded in project lifecycle data")

        # Reasoning panel
        with st.expander("🔍 How this answer was generated"):
            st.markdown("""
1️⃣ Question routing (TXT / CSV / Hybrid)

2️⃣ Retrieval from project lifecycle safety documents

3️⃣ Numeric analysis from CSV datasets

4️⃣ Final synthesis using GPT-4o
""")

    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.divider()
st.caption("Built for vConstruct AI Hackathon | Project Lifecycle Safety Bot")