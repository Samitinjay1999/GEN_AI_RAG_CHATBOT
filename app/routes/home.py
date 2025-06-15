from flask import Blueprint, request, session, jsonify
from config import ADMIN_USERNAME, ADMIN_PASSWORD
import logging

logger = logging.getLogger(__name__)
home_bp = Blueprint('home', __name__)

# === Login Required Decorator ===
def login_required(f):
    from functools import wraps
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return wraps(f)(wrapper)

# === Login Route ===
@home_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = data.get('username')
    pwd = data.get('password')

    if user == ADMIN_USERNAME and pwd == ADMIN_PASSWORD:
        session['logged_in'] = True
        logger.info(f"User '{user}' logged in successfully.")
        return jsonify({"message": "Login successful."}), 200
    else:
        logger.warning(f"Login attempt failed for username: {user}")
        return jsonify({"error": "Invalid credentials"}), 401

# === Logout Route ===
@home_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    logger.info("User logged out.")
    return jsonify({"message": "Logged out successfully."}), 200

# === Health Check or Landing Endpoint ===
@home_bp.route('/health', methods=['GET'])
def landing():
    return jsonify({"status": "ok", "message": "GenAI RAG Chatbot API is running."}), 200
