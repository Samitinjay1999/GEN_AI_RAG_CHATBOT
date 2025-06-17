from flask import Blueprint, request, session, jsonify
from config import ADMIN_USERNAME, ADMIN_PASSWORD
import logging

# Logger setup for this module
logger = logging.getLogger(__name__)

# Defining a blueprint for home routes
home_bp = Blueprint('home', __name__)

# === Login Required Decorator ===
def login_required(f):
    """
    Decorator to protect routes that require authentication.
    Checks if 'logged_in' flag is set in the session.
    """
    from functools import wraps
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return wraps(f)(wrapper)

# === Login Route ===
@home_bp.route('/login', methods=['POST'])
def login():
    """
    Login route that accepts JSON with 'username' and 'password'.
    Validates against admin credentials from environment config.
    On success, sets session flag and logs the user in.
    """
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
    """
    Logout route that clears the session.
    Protected by the login_required decorator.
    """
    session.clear()
    logger.info("User logged out.")
    return jsonify({"message": "Logged out successfully."}), 200

# === Health Check or Landing Endpoint ===
@home_bp.route('/health', methods=['GET'])
def landing():
    """
    Health check endpoint for monitoring or basic availability check.
    Returns a simple JSON response indicating service status.
    """
    return jsonify({"status": "ok", "message": "GenAI RAG Chatbot API is running."}), 200
