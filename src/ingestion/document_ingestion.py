from pathlib import Path
from typing import List
import logging

from langchain.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document

from config import (
    RAW_DATA_DIR, CHROMA_COLLECTION_NAME, CHROMA_PERSIST_DIRECTORY,
    EMBEDDING_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, OLLAMA_BASE_URL
)

logger = logging.getLogger(__name__)


class DocumentIngestion:
    """Handles document loading, processing, and storage in vector database"""
    
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        
    def load_documents(self) -> List[Document]:
        """Load all documents from raw data directory"""
        documents = []
        
        for file_path in RAW_DATA_DIR.rglob("*"):
            if file_path.is_file():
                try:
                    if file_path.suffix.lower() == '.pdf':
                        loader = PyPDFLoader(str(file_path))
                    elif file_path.suffix.lower() in ['.docx', '.doc']:
                        loader = Docx2txtLoader(str(file_path))
                    elif file_path.suffix.lower() == '.txt':
                        loader = TextLoader(str(file_path))
                    else:
                        logger.warning(f"Unsupported file type: {file_path}")
                        continue
                    
                    docs = loader.load()
                    documents.extend(docs)
                    logger.info(f"Loaded {len(docs)} documents from {file_path}")
                    
                except Exception as e:
                    logger.error(f"Error loading {file_path}: {e}")
                    
        return documents
    
    def process_and_store(self):
        """Complete ingestion pipeline"""
        logger.info("Starting document ingestion...")
        
        # Load documents
        documents = self.load_documents()
        if not documents:
            logger.warning("No documents found to process")
            return
        
        # Split documents into chunks
        logger.info(f"Total Documents: {len(documents)}")
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Split into {len(chunks)} chunks")
        
        # Create or update vector store
        vectorstore = Chroma(
            collection_name=CHROMA_COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=CHROMA_PERSIST_DIRECTORY
        )
        
        # Add documents to vector store
        vectorstore.add_documents(chunks)
        vectorstore.persist()
        
        logger.info(f"Successfully ingested {len(chunks)} chunks into vector store")
        return vectorstore
