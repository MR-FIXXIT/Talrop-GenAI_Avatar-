import streamlit as st
import os
from main import RAGChatbot, PERSONALITIES
from langchain_core.messages import HumanMessage, AIMessage

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot - AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium, modern design
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Glassmorphism container */
    .main .block-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: white !important;
        font-weight: 700 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Chat messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        margin: 10px 0 !important;
        padding: 15px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }
    
    .stChatMessage:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* User message */
    [data-testid="stChatMessageContent"] {
        color: white !important;
    }
    
    /* Input box */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        background: rgba(255, 255, 255, 0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Select box */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.8) !important;
        font-weight: 500 !important;
    }
    
    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.25) !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.5);
    }
    
    /* Labels */
    label {
        color: white !important;
        font-weight: 500 !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
    st.session_state.initialized = False

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

# Sidebar
with st.sidebar:
    st.title("🤖 RAG Chatbot")
    st.markdown("---")
    
    # API Key Configuration
    st.subheader("🔑 API Configuration")
    
    # Check if API key is already set
    current_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
    
    if current_api_key:
        st.success("✅ API Key is configured")
        if st.button("Update API Key", use_container_width=True):
            st.session_state.show_api_input = True
    else:
        st.warning("⚠️ API Key not found")
        st.session_state.show_api_input = True
    
    # Show API key input if needed
    if st.session_state.get('show_api_input', False) or not current_api_key:
        api_key_input = st.text_input(
            "HuggingFace API Token",
            type="password",
            placeholder="Enter your HuggingFace API token...",
            help="Get your token from https://huggingface.co/settings/tokens"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save", use_container_width=True):
                if api_key_input:
                    os.environ["HUGGINGFACEHUB_API_TOKEN"] = api_key_input
                    # Also save to .env file
                    with open(".env", "w") as f:
                        f.write(f"HUGGINGFACEHUB_API_TOKEN={api_key_input}\n")
                    # Reload environment variables
                    from dotenv import load_dotenv
                    load_dotenv(override=True)
                    st.success("✅ API Key saved!")
                    st.session_state.show_api_input = False
                    st.rerun()
                else:
                    st.error("❌ Please enter an API key")
        
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_api_input = False
                st.rerun()
        
        st.info("💡 Get your free API token from [HuggingFace](https://huggingface.co/settings/tokens)")
    
    st.markdown("---")
    
    # Personality selector
    st.subheader("🎭 Personality")
    personality_options = {key: value['name'] for key, value in PERSONALITIES.items()}
    
    selected_personality = st.selectbox(
        "Choose personality",
        options=list(personality_options.keys()),
        format_func=lambda x: personality_options[x],
        key="personality_selector"
    )
    
    # Show personality description
    st.caption(PERSONALITIES[selected_personality]['description'])
    
    # Custom personality input
    if selected_personality == "custom":
        custom_prompt = st.text_area(
            "Custom personality prompt",
            placeholder="Enter your custom personality description...",
            key="custom_personality_input"
        )
    
    if st.button("Apply Personality", use_container_width=True):
        if st.session_state.chatbot:
            if selected_personality == "custom":
                st.session_state.chatbot.custom_personality = st.session_state.get("custom_personality_input", "")
            st.session_state.chatbot.set_personality(selected_personality)
            st.success(f"✅ Personality set to: {PERSONALITIES[selected_personality]['name']}")
        else:
            st.warning("⚠️ Please initialize the chatbot first by uploading documents.")
    
    st.markdown("---")
    
    # File upload section
    st.subheader("📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=['pdf', 'txt'],
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    if uploaded_files:
        if st.button("Process Documents", use_container_width=True):
            # Check if API key is set before initializing
            if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
                st.error("❌ Please configure your API key first!")
                st.stop()
            
            with st.spinner("🔄 Processing documents..."):
                # Initialize chatbot if not already done
                if not st.session_state.initialized:
                    try:
                        st.session_state.chatbot = RAGChatbot()
                        st.session_state.initialized = True
                    except Exception as e:
                        st.error(f"❌ Error initializing chatbot: {str(e)}")
                        st.stop()
                
                # Save uploaded files temporarily
                temp_files = []
                for uploaded_file in uploaded_files:
                    temp_path = f"./temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    temp_files.append(temp_path)
                
                # Process documents
                success = st.session_state.chatbot.add_documents(temp_files)
                
                # Clean up temp files
                for temp_file in temp_files:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                
                if success:
                    st.session_state.uploaded_files.extend([f.name for f in uploaded_files])
                    st.success("✅ Documents processed successfully!")
                    st.rerun()
    
    st.markdown("---")
    
    # Statistics
    st.subheader("📊 Statistics")
    if st.session_state.chatbot and st.session_state.chatbot.vectorstore:
        try:
            chunk_count = len(st.session_state.chatbot.vectorstore.get()["documents"])
            file_count = len(st.session_state.chatbot.processed_files)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Chunks", chunk_count)
            with col2:
                st.metric("Files", file_count)
        except:
            st.info("No documents loaded yet")
    else:
        st.info("No documents loaded yet")
    
    st.markdown("---")
    
    # Actions
    st.subheader("⚙️ Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            if st.session_state.chatbot:
                st.session_state.chatbot.messages = []
            st.rerun()
    
    with col2:
        if st.button("💣 Clear DB", use_container_width=True):
            if st.session_state.chatbot:
                st.session_state.chatbot.clear_database()
                st.session_state.messages = []
                st.session_state.uploaded_files = []
                st.success("✅ Database cleared!")
                st.rerun()
    
    st.markdown("---")
    
    # Uploaded files list
    if st.session_state.uploaded_files:
        with st.expander("📄 Uploaded Files"):
            for file in st.session_state.uploaded_files:
                st.text(f"• {file}")

# Main content
st.title("💬 AI Chat Assistant")
st.markdown("### Ask questions about your documents")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about your documents..."):
    if not st.session_state.initialized or not st.session_state.chatbot:
        st.warning("⚠️ Please upload and process documents first!")
    elif not st.session_state.chatbot.conversation:
        st.warning("⚠️ Please upload and process documents first!")
    else:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                response = st.session_state.chatbot.chat(prompt)
                st.markdown(response)
        
        # Add assistant message to chat
        st.session_state.messages.append({"role": "assistant", "content": response})

# Welcome message
if not st.session_state.messages:
    st.info("👋 Welcome! Upload some documents using the sidebar to get started.")
