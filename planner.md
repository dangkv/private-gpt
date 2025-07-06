# 🧠 LLM Chatbot with RAG – Project Plan

> Local/private document-based chatbot using Streamlit, Langchain, Ollama (Mixtral), and ChromaDB

---

## 🧭 Project Goal

Build a private, local chatbot that can answer questions based on PDF/text/image documents using Retrieval-Augmented Generation (RAG).

---

## 📦 Tech Stack

| Component     | Tool              |
|---------------|-------------------|
| Interface     | Streamlit         |
| LLM           | Ollama (Mixtral)  |
| Vector DB     | ChromaDB          |
| RAG Logic     | Langchain         |
| Embeddings    | Ollama / Nomic    |
| File Parsing  | PyPDF / OCR / Unstructured |

---

## 📌 Milestone 1: Environment & Infrastructure Setup

### ✅ Tasks

- [x] Create Python virtual environment
- [x] Install dependencies: `streamlit`, `langchain`, `chromadb`, `ollama`, `PyPDF2` or `unstructured`
- [x] Install and run Ollama + pull `mixtral`
- [ ] Pull embedding model (`nomic-embed-text` or similar)
- [ ] Set up project structure:

```
/chatbot-rag
├── app.py
├── ingest.py
├── data/
├── chroma_db/
├── requirements.txt
├── PROJECT_PLAN.md
```

---

## 📌 Milestone 2: Document Ingestion & Vectorization

### ✅ Tasks

- [ ] Create `ingest.py` script:
  - [ ] Load files from `/data/`
  - [ ] Parse PDF/image/text docs
  - [ ] Chunk documents with `RecursiveCharacterTextSplitter`
  - [ ] Embed with `OllamaEmbeddings`
  - [ ] Store vectors in ChromaDB with `persist_directory`
- [ ] Reload vectorstore and verify embeddings work after restart

---

## 📌 Milestone 3: RAG Chain Construction

### ✅ Tasks

- [ ] Initialize retriever: `vectorstore.as_retriever()`
- [ ] Connect Mixtral LLM via `Ollama(model="mixtral")`
- [ ] Set up Langchain `RetrievalQA` or `ConversationalRetrievalChain`
- [ ] Add logging or Langchain tracing to monitor pipeline
- [ ] Test response for a few known queries

---

## 📌 Milestone 4: Streamlit UI

### ✅ Tasks

- [ ] Build basic chat UI:
  - [ ] Input box for user queries
  - [ ] Display bot responses
  - [ ] Display document sources/references
- [ ] Add document upload via `st.file_uploader`
- [ ] Connect input to Langchain chain and display output
- [ ] Add loading animation or progress bar

---

## 📌 Milestone 5: Enhancements & Features

### 🚀 Optional Tasks

- [ ] Add memory (e.g., `ConversationBufferMemory`)
- [ ] Render output in markdown (bold, lists, code)
- [ ] Add sidebar settings (chunk size, model name, debug mode)
- [ ] Add support for image files with OCR (e.g., `pytesseract`)
- [ ] Show list of uploaded/processed documents

---

## 📌 Milestone 6: Testing & Packaging

### ✅ Tasks

- [ ] Create test script to validate response pipeline
- [ ] Ensure ChromaDB persists and reloads embeddings
- [ ] Add `config.yaml` or `.env` for model & path settings
- [ ] Add `Makefile` or `start.sh` script for one-line startup

---

## 📌 Milestone 7: (Optional) Dockerization & Deployment

### 🐳 Tasks

- [ ] Create a `Dockerfile` based on `python:3.11-slim`
- [ ] Install Ollama and copy data/model files
- [ ] Mount volumes for document folder and chroma DB
- [ ] Expose port 8501 for Streamlit
- [ ] Build and run Docker image

---

## 📝 Notes

- Mixtral is heavy (~40GB). Use `mistral` or `llama2` for lighter local testing.
- Chroma stores everything locally (no server needed).
- DuckDB (used by Chroma) is embedded and doesn’t need setup.
- Ensure `persist_directory` is consistent to avoid re-embedding.
- nomic-embed-text only embeds texts and pdfs. Cannot embed images.
- apply hashing to documents to prevent duplication in vector db with the same files.

---


