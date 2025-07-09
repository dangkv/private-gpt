import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from src.pipeline.rag_pipeline import RAGPipeline

# App config
st.set_page_config(page_title="Streamlit Chatbot", page_icon="🤖")
st.title("PrivateGPT")

# iMessage Theme
st.markdown("""
    <style>
    html, body, [data-testid="stApp"] {
        background-color: #1c1c1e;
        color: #ffffff;
    }

    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 0.5rem 1rem;
    }

    .bubble {
        max-width: 75%;
        padding: 10px 14px;
        border-radius: 18px;
        font-size: 16px;
        line-height: 1.4;
        word-wrap: break-word;
        box-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }

    .user-bubble {
        background-color: #007aff; /* iMessage blue */
        color: white;
        align-self: flex-end;
        border-bottom-right-radius: 4px;
    }

    .assistant-bubble {
        background-color: #2c2c2e;
        color: #d1d1d6;
        align-self: flex-start;
        border-bottom-left-radius: 4px;
    }

    input, textarea {
        background-color: #2c2c2e !important;
        color: white !important;
    }

    label[data-testid="stChatInputLabel"] {
        color: #aaaaaa;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_rag_pipeline():
    """Load RAG pipeline (cached for performance)"""
    return RAGPipeline()

def get_response(user_query, chat_history, rag:RAGPipeline):

    result = rag.query_stream(user_query)

    return result["answer_stream"]

def render_message(role: str, content: str):
    bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
    st.markdown(
        f"""
        <div class="chat-container">
            <div class="bubble {bubble_class}">{content}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hello, I am a bot. How can I help you?")
    ]

# Load RAG pipeline
try:
    rag = load_rag_pipeline()
    
    # Health check
    health = rag.health_check()
    if not health["retrieval"]:
        st.error("⚠️ Vector store not initialized. Please run document ingestion first.")
        st.code("python scripts/ingest_documents.py")

except Exception as e:
    st.error(f"Failed to initialize RAG system: {e}")

# Render past messages with dark bubbles
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
# Display past messages, one flex row per message
for msg in st.session_state.chat_history:

    if isinstance(msg, HumanMessage):
        render_message("user", msg.content)
    elif isinstance(msg, AIMessage):
        render_message("assistant", msg.content)

st.markdown('</div>', unsafe_allow_html=True)

# User input
user_query = st.chat_input("Type your message here...")
if user_query:
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    st.markdown(
        f'<div class="chat-container"><div class="bubble user-bubble">{user_query}</div></div>',
        unsafe_allow_html=True
    )

    full_response = ""
    with st.empty():
        for chunk in get_response(user_query, st.session_state.chat_history, rag):
            full_response += chunk
            st.markdown(
                f'<div class="chat-container"><div class="bubble assistant-bubble">{full_response}</div></div>',
                unsafe_allow_html=True
            )

    st.session_state.chat_history.append(AIMessage(content=full_response))
