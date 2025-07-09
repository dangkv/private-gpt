# 🔒 PrivateGPT - Your Personal AI Assistant

<div align="center">

![PrivateGPT Logo](https://img.shields.io/badge/🤖-PrivateGPT-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)

*Chat with your documents privately, locally, and securely* ✨

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## 🌟 What is PrivateGPT?

PrivateGPT transforms your personal documents into an intelligent, conversational AI assistant. Unlike cloud-based solutions, **everything runs locally** on your machine, ensuring your sensitive data never leaves your control.

### 🚀 Why PrivateGPT?

- **🔐 Complete Privacy**: Your documents never leave your machine
- **📚 Smart Document Understanding**: Chat with PDFs, Word docs, and text files
- **⚡ Real-time Responses**: Streaming responses for better user experience
- **🎯 Context-Aware**: Provides accurate answers based on your documents
- **🛠️ Easy Setup**: Simple installation and intuitive interface

---

## ✨ Features

### 🔍 **Intelligent Document Processing**
- Supports multiple formats: PDF, DOCX, DOC, TXT
- Automatic text chunking for optimal retrieval
- Vector embeddings for semantic search

### 💬 **Natural Conversation**
- Streamlit-based chat interface with design first philosophy
- Real-time streaming responses
- Context-aware conversations
- Emoji support for better readability

### 🏗️ **Robust Architecture**
- RAG (Retrieval-Augmented Generation) pipeline
- ChromaDB for vector storage
- Ollama for local LLM inference
- Modular and extensible design

---

## 🛠️ Installation

### Prerequisites

Before getting started, ensure you have the following installed:

- **Python 3.8+** 🐍
- **Ollama** (for local LLM inference) 🤖
- **Homebrew** (for macOS users) 🍺

### Step 1: Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows (using WSL)
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Download Required Models

```bash
# Download the embedding model
ollama pull nomic-embed-text

# Download the language model
ollama pull mistral
```

### Step 3: Clone and Setup PrivateGPT

```bash
# Clone the repository
git clone https://github.com/yourusername/privateGPT.git
cd privateGPT

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Create requirements.txt

```txt
streamlit>=1.28.0
langchain>=0.0.350
langchain-community>=0.0.10
chromadb>=0.4.15
ollama>=0.1.0
pypdf>=3.17.0
python-docx>=0.8.11
docx2txt>=0.8
```

---

## 📁 Data Folder Structure

Understanding the data folder structure is crucial for setting up PrivateGPT:

```
data/
├── raw/                    # 📄 Your unstructured documents go here
│   ├── document1.pdf
│   ├── report.docx
│   ├── notes.txt
│   └── subfolder/
│       └── more_docs.pdf
├── processed/              # 🔧 Processed document chunks (auto-generated)
└── chroma_db/             # 🗄️ Vector database storage (auto-generated)
    ├── chroma.sqlite3
    └── index/
```

### 📋 Setting Up Your Documents

1. **Create the data directory** (if it doesn't exist):
   ```bash
   mkdir -p data/raw
   ```

2. **Add your documents** to the `data/raw/` folder:
   - Supported formats: `.pdf`, `.docx`, `.doc`, `.txt`
   - You can organize documents in subfolders
   - No size limit (within reason)

3. **Example structure**:
   ```
   data/raw/
   ├── company_policies/
   │   ├── employee_handbook.pdf
   │   └── code_of_conduct.docx
   ├── research_papers/
   │   ├── ai_trends_2024.pdf
   │   └── machine_learning_guide.pdf
   └── personal_notes/
       ├── meeting_notes.txt
       └── project_ideas.docx
   ```

---

## 🚀 Usage

### Quick Start

1. **Start the services**:
   ```bash
   make start
   ```

2. **Ingest your documents**:
   ```bash
   make db-ingest
   ```

3. **Open your browser** and go to `http://localhost:8501`

4. **Start chatting** with your documents! 💬

5. **Shut down bot**:
   ```bash
   make stop
   ```

### Available Commands

PrivateGPT comes with a comprehensive Makefile for easy management:

```bash
# 🎯 Main Commands
make start          # Start all services
make stop           # Stop all services
make status         # Check service status

# 📊 Streamlit Management
make streamlit-start    # Start Streamlit app
make streamlit-stop     # Stop Streamlit app
make streamlit-reset    # Restart Streamlit

# 🤖 Ollama Management
make llm-start      # Start Ollama service
make llm-stop       # Stop Ollama service
make llm-status     # Check Ollama status

# 🗄️ Database Management
make db-ingest      # Process and ingest documents
make db-reset       # Reset database
make db-backup      # Create database backup
make db-check       # Check database status

# 🧹 Cleanup
make clean          # Clean temporary files
make clean-all      # Deep clean everything
```

### Manual Document Ingestion

If you prefer to run the ingestion manually:

```bash
python scripts/ingest_documents.py
```

---

## 🏗️ Architecture

PrivateGPT follows a modular RAG (Retrieval-Augmented Generation) architecture:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   📄 Documents   │ ── │  📝 Ingestion   │ ── │  🗄️ Vector DB   │
│   (PDF, DOCX,   │    │  (Chunking &    │    │  (ChromaDB)    │
│    TXT files)   │    │   Embedding)    │    │                │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  💬 Streamlit   │ ── │  🧠 RAG         │ ── │  🔍 Retrieval   │
│   Interface     │    │  Pipeline       │    │   (Semantic     │
│                 │    │                 │    │    Search)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │  🤖 Generation  │
                       │   (Ollama +     │
                       │    Mistral)     │
                       └─────────────────┘
```

### Key Components

- **🔄 Ingestion Pipeline**: Processes documents and creates vector embeddings
- **🔍 Retrieval System**: Finds relevant document chunks using semantic search
- **🤖 Generation Engine**: Uses Ollama with Mistral model for response generation
- **💬 Chat Interface**: Streamlit-based UI with real-time streaming
- **🗄️ Vector Database**: ChromaDB for efficient similarity search

---

## 🔧 Configuration

Customize PrivateGPT by modifying `config.py`:

```python
# Model configurations
EMBEDDING_MODEL = "nomic-embed-text"    # Change embedding model
LLM_MODEL = "mistral"                   # Change language model
OLLAMA_BASE_URL = "http://localhost:11434"

# Chunking parameters
CHUNK_SIZE = 1000                       # Adjust chunk size
CHUNK_OVERLAP = 200                     # Adjust overlap

# Retrieval parameters
TOP_K_RETRIEVAL = 5                     # Number of documents to retrieve
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **🍴 Fork the repository**
2. **🌿 Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **💾 Commit your changes**: `git commit -m 'Add amazing feature'`
4. **📤 Push to the branch**: `git push origin feature/amazing-feature`
5. **🔄 Open a Pull Request**

### 📝 Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Include type hints where appropriate
- Write unit tests for new features
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **LangChain** for the RAG framework
- **Ollama** for local LLM inference
- **ChromaDB** for vector storage
- **Streamlit** for the web interface
- **Mistral** for the language model

---

<div align="center">

**🎉 Ready to chat with your documents privately?**

[Get Started](#-installation) • [View Demo](https://demo.privategpt.com) • [Join Community](https://discord.gg/privategpt)

Made with ❤️ by the PrivateGPT Team

</div>