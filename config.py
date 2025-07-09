import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
VECTORDB_DIR = DATA_DIR / "chroma_db"

# Ensure directories exist
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, VECTORDB_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Model configurations
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "mistral"
OLLAMA_BASE_URL = "http://localhost:11434"

# ChromaDB settings
CHROMA_COLLECTION_NAME = "document_store"
CHROMA_PERSIST_DIRECTORY = str(VECTORDB_DIR)

# Chunking parameters
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval parameters
TOP_K_RETRIEVAL = 5
