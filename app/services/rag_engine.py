import logging
from app.services.embedding import get_embedding, generate_gemini_response
from app.services.chromadb_service import query_chunks

logger = logging.getLogger(__name__)

# === RAG Orchestration ===
def answer_query(user_query, top_k=5):
    logger.info("Starting RAG pipeline for query.")
    
    # Step 1: Embed query
    query_embedding = get_embedding(user_query)
    if not query_embedding:
        return "Could not generate embedding for your query.", []

    # Step 2: Retrieve relevant chunks from ChromaDB
    retrieved_chunks = query_chunks(query_embedding, top_k=top_k)
    if not retrieved_chunks:
        return "No relevant information found.", []

    # Step 3: Send context + query to Gemini for final response
    final_answer = generate_gemini_response(user_query, retrieved_chunks)
    
    logger.info("RAG response generated.")
    return final_answer, retrieved_chunks
