from typing import List, Dict, Any, Iterator, Optional, Callable
import logging

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema import Document
from langchain_core.messages import HumanMessage, AIMessage

from config import LLM_MODEL, OLLAMA_BASE_URL

logger = logging.getLogger(__name__)


class ResponseGeneration:
    """Handles response generation using LLM with context from retrieved documents and chat history"""
    
    def __init__(self):
        self.llm = ChatOllama(
            model=LLM_MODEL,
            base_url=OLLAMA_BASE_URL
        )
        self.output_parser = StrOutputParser()
        
        # RAG prompt template with chat history
        self.prompt_template = ChatPromptTemplate.from_template("""You are a helpful assistant that answers questions based on the provided context and chat history.

Context:
{context}

Chat History:
{chat_history}

Current Question: {question}

Instructions:
- Answer the question based on the context provided and previous conversation
- If the context doesn't contain enough information to answer the question, say so
- Be concise and accurate
- Cite specific information from the context when relevant
- Reply to human social conversations naturally
- If the question and the context are unrelated, specify that it's not clear
- Format the answers so that they are easy to read. Use indents, point forms or spacings
- Encourage the use of Emojis if it helps with answer clarity
- Consider the chat history to provide contextual responses

Answer:""")
    
    def _format_chat_history(self, chat_history: List) -> str:
        """Format chat history for inclusion in prompt"""
        if not chat_history:
            return "No previous conversation."
        
        formatted_history = []
        for message in chat_history[-10:]:  # Keep last 10 messages to avoid token limit
            if isinstance(message, HumanMessage):
                formatted_history.append(f"Human: {message.content}")
            elif isinstance(message, AIMessage):
                formatted_history.append(f"Assistant: {message.content}")
        
        return "\n".join(formatted_history)
    
    def generate_response_stream(self, query: str, relevant_docs: List[Document], 
                               chat_history: List = None) -> Iterator[str]:
        """Generate streaming response using retrieved documents and chat history"""
        try:
            # Combine relevant documents into context
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Format chat history
            formatted_history = self._format_chat_history(chat_history or [])
            
            # Create the chain
            chain = self.prompt_template | self.llm | self.output_parser
            
            # Stream the response
            for chunk in chain.stream({
                "context": context,
                "question": query,
                "chat_history": formatted_history
            }):
                yield chunk
                
            logger.info("Streaming response generated successfully")
            
        except Exception as e:
            logger.error(f"Error generating streaming response: {e}")
            yield f"I apologize, but I encountered an error while generating a response: {str(e)}"
