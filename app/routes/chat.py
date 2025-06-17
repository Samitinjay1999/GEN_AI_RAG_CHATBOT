from flask import Blueprint, request, jsonify, session
from app.routes.home import login_required
from app.services.rag_engine import answer_query
import logging

# get logger for chat routes
logger = logging.getLogger(__name__)
chat_bp = Blueprint("chat", __name__)

# === Chat API ===
@chat_bp.route("/chat", methods=["POST"])
@login_required
def chat():
    """
    Chat endpoint that handles POST requests with a user's query.
    - Requires authentication.
    - Uses RAG engine to get a response and the most relevant document chunks.
    - Stores chat history in the session.
    Returns:
        JSON with bot response, used chunks, and chat history.
    """
    data = request.get_json()
    query = data.get("query")

    # Validate the input query 
    if not query:
        logger.warning("Empty query received.")
        return jsonify({"error": "Query is required"}), 400
    # Log the received query
    logger.info(f"Received query: {query}")

    # === Get both the answer and top_k relevant chunks ===
    answer, used_chunks = answer_query(query)
    # logger.info(f"Used Chunks: {used_chunks}")
    # logger.info(f"Query Response : {answer}")

    # === Save to session history ===
    history = session.get("chat_history", [])
    # logger.info(f"Chat History: {history}")
    history.append({"user": query, "bot": answer})
    
    session["chat_history"] = history
    # Return answer used chunks and history as json response 
    return jsonify({
        "response": answer,
        "chunks_used": used_chunks,
        "history": history
    }), 200
