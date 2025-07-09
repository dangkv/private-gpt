from typing import List, Dict, Any, Iterator, Optional, Callable
import logging

from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import BaseCallbackHandler

from config import LLM_MODEL, OLLAMA_BASE_URL

logger = logging.getLogger(__name__)


class CustomStreamingCallbackHandler(BaseCallbackHandler):
    """Custom callback handler for streaming responses"""
    
    def __init__(self, callback_fn: Optional[Callable[[str], None]] = None):
        self.callback_fn = callback_fn
        self.tokens = []
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Called when a new token is generated"""
        self.tokens.append(token)
        if self.callback_fn:
            self.callback_fn(token)
    
    def get_full_response(self) -> str:
        """Get the complete response"""
        return "".join(self.tokens)


class ResponseGeneration:
    """Handles response generation using LLM with context from retrieved documents"""
    
    def __init__(self):
        self.llm = Ollama(
            model=LLM_MODEL,
            base_url=OLLAMA_BASE_URL
        )
        
        # RAG prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful assistance. that answers questions based on the provided context.

Context:
{context}

Question: {question}

Instructions:
- Answer the question based on the context provided
- If the context doesn't contain enough information to answer the question, say so
- Be concise and accurate
- Cite specific information from the context when relevant
- Reply to human social conversations
- If the question and the context are unrelated, specify that is not clear
- Format the answers so that it easy to read. Indents, point forms or spacings
- Encourage the use of Emojis if it helps with answer clarity

Answer:"""
        )
    
    def generate_response(self, query: str, relevant_docs: List[Document]) -> str:
        """Generate response using retrieved documents (non-streaming)"""
        try:
            # Combine relevant documents into context
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Format prompt
            prompt = self.prompt_template.format(
                context=context,
                question=query
            )
            
            # Generate response
            response = self.llm(prompt)
            
            logger.info("Response generated successfully")
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error while generating a response: {str(e)}"
    
    def generate_response_stream(self, query: str, relevant_docs: List[Document], 
                               callback_fn: Optional[Callable[[str], None]] = None) -> Iterator[str]:
        """Generate streaming response using retrieved documents"""
        try:
            # Combine relevant documents into context
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Format prompt
            prompt = self.prompt_template.format(
                context=context,
                question=query
            )
            
            # Create streaming callback handler
            streaming_handler = CustomStreamingCallbackHandler(callback_fn)
            
            # Create LLM with streaming enabled
            streaming_llm = Ollama(
                model=LLM_MODEL,
                base_url=OLLAMA_BASE_URL,
                callbacks=[streaming_handler]
            )
            
            # Generate response with streaming
            streaming_llm(prompt)
            
            # Yield tokens as they come
            for token in streaming_handler.tokens:
                yield token
                
            logger.info("Streaming response generated successfully")
            
        except Exception as e:
            logger.error(f"Error generating streaming response: {e}")
            yield f"I apologize, but I encountered an error while generating a response: {str(e)}"
