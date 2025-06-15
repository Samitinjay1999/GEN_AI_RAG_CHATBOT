from flask import Blueprint, request, jsonify, session
from app.routes.home import login_required
from app.services.rag_engine import answer_query
import logging

logger = logging.getLogger(__name__)
chat_bp = Blueprint("chat", __name__)

# === Chat API ===
@chat_bp.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    query = data.get("query")

    if not query:
        logger.warning("Empty query received.")
        return jsonify({"error": "Query is required"}), 400

    logger.info(f"Received query: {query}")

    # === Get both the answer and top_k relevant chunks ===
    answer, used_chunks = answer_query(query)

    # === Save to session history ===
    history = session.get("chat_history", [])
    history.append({"user": query, "bot": answer})
    session["chat_history"] = history

    return jsonify({
        "response": answer,
        "chunks_used": used_chunks,
        "history": history
    }), 200
