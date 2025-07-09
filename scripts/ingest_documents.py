#!/usr/bin/env python3
"""
Standalone script to ingest documents into the RAG system
Run this script whenever you add new documents to the data/raw directory
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.ingestion import DocumentIngestion

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main ingestion process"""
    logger = logging.getLogger(__name__)
    
    logger.info("Starting document ingestion process...")
    
    try:
        # Initialize ingestion
        ingestion = DocumentIngestion()
        
        # Process and store documents
        vectorstore = ingestion.process_and_store()
        
        if vectorstore:
            logger.info("✅ Document ingestion completed successfully!")
            logger.info("You can now query your documents using the RAG system.")
        else:
            logger.warning("⚠️  No documents were processed. Check if documents exist in data/raw/")
            
    except Exception as e:
        logger.error(f"❌ Document ingestion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
