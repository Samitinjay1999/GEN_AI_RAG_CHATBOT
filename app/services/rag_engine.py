import logging
from app.services.embedding import get_embedding, generate_gemini_response
from app.services.chromadb_service import query_chunks

logger = logging.getLogger(__name__)

# === RAG Orchestration ===
def answer_query(user_query, top_k=5):
    """
    Orchestrates the RAG (Retrieval-Augmented Generation) pipeline.

    Steps:
    1. Generate an embedding for the user's query.
    2. Retrieve top-k relevant chunks from ChromaDB using the query embedding.
    3. Send the query and retrieved context to the Gemini model to generate a response.

    Args:
        user_query (str): The question or query provided by the user.
        top_k (int): Number of most relevant document chunks to retrieve.

    Returns:
        tuple: (final_answer, retrieved_chunks)
            - final_answer (str): The generated answer from Gemini.
            - retrieved_chunks (list): List of top-k relevant text chunks used for context.
    """
    logger.info("Starting RAG pipeline for query.")
    
    # Step 1: Embed the user query
    query_embedding = get_embedding(user_query)
    if not query_embedding:
        return "Could not generate embedding for your query.", []

    # Step 2: Retrieve relevant chunks from ChromaDB(top k)
    retrieved_chunks = query_chunks(query_embedding, top_k=top_k)
    if not retrieved_chunks:
        return "No relevant information found.", []

    # Step 3: Send context + query to Gemini model for final response
    final_answer = generate_gemini_response(user_query, retrieved_chunks)
    
    logger.info("RAG response generated.")
    return final_answer, retrieved_chunks
