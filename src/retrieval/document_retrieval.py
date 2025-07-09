from typing import List
import logging

from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document

from config import (
    CHROMA_COLLECTION_NAME, CHROMA_PERSIST_DIRECTORY,
    EMBEDDING_MODEL, TOP_K_RETRIEVAL, OLLAMA_BASE_URL
)

logger = logging.getLogger(__name__)


class DocumentRetrieval:
    """Handles document retrieval from vector database using semantic search"""
    
    def __init__(self):
        self.embeddings = OllamaEmbeddings(
            model=EMBEDDING_MODEL,
            base_url=OLLAMA_BASE_URL
        )
        self.vectorstore = None
        self._initialize_vectorstore()
        
    def _initialize_vectorstore(self):
        """Initialize connection to existing vector store"""
        try:
            self.vectorstore = Chroma(
                collection_name=CHROMA_COLLECTION_NAME,
                embedding_function=self.embeddings,
                persist_directory=CHROMA_PERSIST_DIRECTORY
            )
            logger.info("Vector store initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise
    
    def retrieve_documents(self, query: str, k: int = TOP_K_RETRIEVAL) -> List[Document]:
        """Retrieve relevant documents for a query"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        
        try:
            # Perform similarity search
            relevant_docs = self.vectorstore.similarity_search(
                query, 
                k=k
            )
            
            logger.info(f"Retrieved {len(relevant_docs)} relevant documents")
            return relevant_docs
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def get_retriever(self):
        """Get retriever interface for the vector store"""
        if not self.vectorstore:
            raise ValueError("Vector store not initialized")
        
        return self.vectorstore.as_retriever(
            search_kwargs={"k": TOP_K_RETRIEVAL}
        )
