import os
import json
import logging
from pathlib import Path
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)

def load_and_embed_articles():
    logger.info("Loading articles for knowledge base...")
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
    
    logger.info(f"Loaded {len(documents)} articles for embedding")

    # Initialize embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )

    # Create Chroma vector store
    logger.info("Creating vector store with embeddings...")
    vectorstore = Chroma.from_documents(documents, embeddings)
    logger.info("Knowledge base initialized successfully")
    return vectorstore.as_retriever()

retriever = load_and_embed_articles()

def knowledge_base_tool(query: str):
    """Searches the knowledge base for answers to customer questions."""
    logger.info(f"KB Tool: Searching for query: {query[:100]}...")
    results = retriever.invoke(query)
    logger.info(f"KB Tool: Found {len(results) if results else 0} results")
    return results

