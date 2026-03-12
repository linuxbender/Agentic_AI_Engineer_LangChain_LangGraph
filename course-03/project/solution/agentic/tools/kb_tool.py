import os
import json
import logging
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from agentic.logging_config import get_structured_logger

logger = get_structured_logger(__name__)

def load_and_embed_articles():
    logger.info("Loading articles for knowledge base", tool_name="kb_tool")
    # Get the directory where this file is located
    current_dir = Path(__file__).parent.parent.parent
    file_path = current_dir / 'data' / 'external' / 'cultpass_articles.jsonl'
    
    # Load JSONL file
    documents = []
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            # Create Document from JSON line
            doc = Document(
                page_content=data.get('content', json.dumps(data)),
                metadata=data
            )
            documents.append(doc)
    
    logger.info(
        "Articles loaded",
        tool_name="kb_tool",
        document_count=len(documents)
    )

    # Initialize embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )

    # Create Chroma vector store
    logger.info("Creating vector store with embeddings", tool_name="kb_tool")
    vectorstore = Chroma.from_documents(documents, embeddings)
    logger.info("Knowledge base initialized successfully", tool_name="kb_tool")
    return vectorstore.as_retriever()

retriever = load_and_embed_articles()

def knowledge_base_tool(query: str):
    """Searches the knowledge base for answers to customer questions."""
    logger.info(
        "KB Tool search initiated",
        tool_name="kb_tool",
        query_preview=query[:100]
    )
    
    try:
        results = retriever.invoke(query)
        logger.info(
            "KB Tool search completed",
            tool_name="kb_tool",
            results_count=len(results) if results else 0
        )
        return results
    except Exception as e:
        logger.error(
            "KB Tool search failed",
            tool_name="kb_tool",
            error_details=str(e)
        )
        return []
