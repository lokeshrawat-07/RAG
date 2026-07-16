import streamlit as st
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DocMind – RAG Assistant",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #0d0f14;
    --surface:   #13161e;
    --border:    #1f2330;
    --accent:    #e8c87d;
    --accent2:   #7db8e8;
    --text:      #e8eaf0;
    --muted:     #6b7280;
    --user-bg:   #1a2235;
    --ai-bg:     #1a1f2e;
    --radius:    14px;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}
.stApp { background-color: var(--bg); }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Sidebar header ── */
.sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.6rem;
    color: var(--accent) !important;
    letter-spacing: -0.02em;
    padding: 0.5rem 0 1.5rem;
    line-height: 1.1;
}
.sidebar-brand span { color: var(--accent2) !important; }

/* ── Status badge ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}
.status-ready  { background: #1a2e1a; color: #6fcf7a; border: 1px solid #2a4a2a; }
.status-empty  { background: #2e1a1a; color: #cf6f6f; border: 1px solid #4a2a2a; }

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    background: #0d1117 !important;
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--accent) !important;
    color: #0d0f14 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.55rem 1.4rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}

/* ── Main page title ── */
.page-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    color: var(--text);
    letter-spacing: -0.03em;
    margin-bottom: 0.2rem;
}
.page-subtitle {
    font-size: 0.95rem;
    color: var(--muted);
    margin-bottom: 2rem;
}

/* ── Chat container ── */
.chat-wrap {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    padding: 1rem 0;
}

/* ── Message bubbles ── */
.msg {
    display: flex;
    gap: 14px;
    align-items: flex-start;
}
.msg-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.avatar-user { background: var(--user-bg); border: 1px solid #2a3a55; }
.avatar-ai   { background: #1e1a2e; border: 1px solid #2a2545; }
.msg-bubble {
    padding: 0.8rem 1.1rem;
    border-radius: 0 var(--radius) var(--radius) var(--radius);
    font-size: 0.93rem;
    line-height: 1.65;
    max-width: 90%;
}
.bubble-user { background: var(--user-bg); border: 1px solid #1f2f4a; color: var(--accent2); }
.bubble-ai   { background: var(--ai-bg);   border: 1px solid #1f1f38; color: var(--text); }
.msg-label { font-size: 0.72rem; color: var(--muted); margin-bottom: 4px; font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase; }

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Input ── */
.stTextInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    padding: 0.65rem 1rem !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(232,200,125,0.15) !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Info / warning boxes ── */
.stInfo, .stWarning, .stSuccess, .stError {
    border-radius: var(--radius) !important;
    border: none !important;
}

/* ── Progress bar ── */
.stProgress > div > div { background-color: var(--accent) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar       { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── Source expander ── */
details summary {
    color: var(--muted) !important;
    font-size: 0.8rem;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vectorstore_ready" not in st.session_state:
    st.session_state.vectorstore_ready = False
if "doc_name" not in st.session_state:
    st.session_state.doc_name = None


# ── Helpers ───────────────────────────────────────────────────────────────────
PERSIST_DIR = "chroma-db"
EMBED_MODEL  = "sentence-transformers/all-MiniLM-L6-v2"

@st.cache_resource(show_spinner=False)
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)

@st.cache_resource(show_spinner=False)
def get_llm():
    return ChatMistralAI(model="mistral-small-latest")

def ingest_pdf(file_bytes: bytes, filename: str) -> int:
    """Save upload → chunk → embed → persist. Returns chunk count."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    loader   = PyPDFLoader(tmp_path)
    docs     = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks   = splitter.split_documents(docs)

    embeddings = get_embedding_model()
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )
    os.unlink(tmp_path)
    return len(chunks)

def get_retriever():
    embeddings = get_embedding_model()
    vs = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    return vs.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5},
    )

PROMPT = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant.
Use ONLY the provided context to answer the question.
If the answer is not present in the context, say: "I could not find the answer in the document." """),
    ("human", "Context:\n{context}\n\nQuestion:\n{question}"),
])

def ask(query: str):
    retriever = get_retriever()
    docs      = retriever.invoke(query)
    context   = "\n\n".join(d.page_content for d in docs)
    llm       = get_llm()
    response  = llm.invoke(PROMPT.invoke({"context": context, "question": query}))
    return response.content, docs


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">Doc<span>Mind</span></div>', unsafe_allow_html=True)
    st.markdown("---")

    # Status
    if st.session_state.vectorstore_ready:
        st.markdown(
            f'<div class="status-badge status-ready">✦ Ready — {st.session_state.doc_name}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-badge status-empty">○ No document loaded</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Upload
    st.markdown("#### Upload a PDF")
    uploaded = st.file_uploader(
        label="Drop your PDF here",
        type=["pdf"],
        label_visibility="collapsed",
    )

    if uploaded:
        if st.button("⚡  Process Document"):
            with st.spinner("Chunking & embedding…"):
                n = ingest_pdf(uploaded.read(), uploaded.name)
            st.session_state.vectorstore_ready = True
            st.session_state.doc_name = uploaded.name
            st.session_state.chat_history = []
            st.success(f"Done! {n} chunks indexed.")

    st.markdown("---")

    # Clear chat
    if st.button("🗑  Clear Conversation"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:0.75rem;color:#4b5563;">Powered by MistralAI · ChromaDB · LangChain</p>',
        unsafe_allow_html=True,
    )


# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">Ask Your Document</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">Upload a PDF in the sidebar, then ask anything about it.</div>',
    unsafe_allow_html=True,
)

# Chat history
if st.session_state.chat_history:
    st.markdown('<div class="chat-wrap">', unsafe_allow_html=True)
    for turn in st.session_state.chat_history:
        # User bubble
        st.markdown(f"""
        <div class="msg">
            <div class="msg-avatar avatar-user">👤</div>
            <div>
                <div class="msg-label">You</div>
                <div class="msg-bubble bubble-user">{turn["user"]}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # AI bubble
        st.markdown(f"""
        <div class="msg">
            <div class="msg-avatar avatar-ai">✦</div>
            <div>
                <div class="msg-label">DocMind</div>
                <div class="msg-bubble bubble-ai">{turn["ai"]}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # Source chunks expander
        if turn.get("sources"):
            with st.expander("View source chunks"):
                for i, src in enumerate(turn["sources"], 1):
                    st.markdown(
                        f"**Chunk {i}** *(page {src.metadata.get('page', '?')})*\n\n{src.page_content}",
                    )
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.vectorstore_ready:
    st.info("📄 Document loaded. Ask your first question below!")
else:
    st.warning("⬅  Upload a PDF from the sidebar to get started.")

# Input bar (pinned to bottom by placing it last)
st.markdown("---")

if st.session_state.vectorstore_ready:
    col1, col2 = st.columns([8, 1])
    with col1:
        query = st.text_input(
            label="question",
            placeholder="What is this document about?",
            label_visibility="collapsed",
            key="query_input",
        )
    with col2:
        send = st.button("Send", key="send_btn")

    if send and query.strip():
        with st.spinner("Thinking…"):
            answer, sources = ask(query.strip())
        st.session_state.chat_history.append({
            "user": query.strip(),
            "ai": answer,
            "sources": sources,
        })
        st.rerun()