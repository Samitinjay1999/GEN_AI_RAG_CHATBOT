import os
from dotenv import load_dotenv

load_dotenv()

# === Gemini API Config ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
EMBEDDING_URL = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent"
CHAT_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# === ChromaDB Config ===
CHROMADB_COLLECTION = "documents"

# === Upload Config ===
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {'pdf', 'txt'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

# === Logging Config ===
LOG_FILE = "app.log"

# --- Auth ---
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")