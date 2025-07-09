import logging
from typing import Dict, Any

from src.ingestion import DocumentIngestion
from src.retrieval import DocumentRetrieval
from src.generation import ResponseGeneration

logger = logging.getLogger(__name__)

class RAGPipeline:
    """Main RAG pipeline orchestrator"""
    
    def __init__(self):
        self.ingestion = DocumentIngestion()
        self.retrieval = DocumentRetrieval()
        self.generation = ResponseGeneration()
        
    def ingest_documents(self):
        """Run document ingestion process"""
        logger.info("Starting document ingestion...")
        return self.ingestion.process_and_store()
    
    def query(self, question: str, k: int = 5) -> Dict[str, Any]:
        """
        Main query interface for the RAG system
        
        Args:
            question: User's question
            k: Number of documents to retrieve
            
        Returns:
            Dictionary containing answer and metadata
        """
        try:
            # Retrieve relevant documents
            relevant_docs = self.retrieval.retrieve_documents(question, k=k)
            
            if not relevant_docs:
                return {
                    "answer": "I couldn't find any relevant information to answer your question.",
                    "sources": [],
                    "num_sources": 0
                }
            
            # Generate response
            answer = self.generation.generate_response(question, relevant_docs)
            
            # Extract source information
            sources = []
            for doc in relevant_docs:
                source_info = {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                }
                sources.append(source_info)
            
            return {
                "answer": answer,
                "sources": sources,
                "num_sources": len(sources)
            }
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {e}")
            return {
                "answer": f"I encountered an error while processing your question: {str(e)}",
                "sources": [],
                "num_sources": 0
            }

    def query_stream(self, question: str, k: int = 5) -> Dict[str, Any]:
        """
        Streaming query interface for the RAG system
        
        Args:
            question: User's question
            k: Number of documents to retrieve
            
        Returns:
            Dictionary containing streaming answer generator and metadata
        """
        try:
            # Retrieve relevant documents
            relevant_docs = self.retrieval.retrieve_documents(question, k=k)
            
            if not relevant_docs:
                def empty_stream():
                    yield "I couldn't find any relevant information to answer your question."
                
                return {
                    "answer_stream": empty_stream(),
                    "sources": [],
                    "num_sources": 0
                }
            
            # Generate streaming response
            answer_stream = self.generation.generate_response_stream(question, relevant_docs)
            
            # Extract source information
            sources = []
            for doc in relevant_docs:
                source_info = {
                    "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "metadata": doc.metadata
                }
                sources.append(source_info)
            
            return {
                "answer_stream": answer_stream,
                "sources": sources,
                "num_sources": len(sources)
            }
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline streaming: {e}")
            
            def error_stream():
                yield f"I encountered an error while processing your question: {str(e)}"
            
            return {
                "answer_stream": error_stream(),
                "sources": [],
                "num_sources": 0
            }
    
    def health_check(self) -> Dict[str, bool]:
        """Check if all components are working"""
        status = {
            "ingestion": False,
            "retrieval": False,
            "generation": False
        }
        
        try:
            # Check retrieval (most critical for query time)
            if self.retrieval.vectorstore:
                status["retrieval"] = True
            
            # Check generation
            test_response = self.generation.llm("Test")
            if test_response:
                status["generation"] = True
                
            # Ingestion is checked when needed
            status["ingestion"] = True
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            
        return status
