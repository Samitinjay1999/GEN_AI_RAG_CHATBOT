import os
from dotenv import load_dotenv

# Load environment variable from the .env file
load_dotenv()

# === Gemini API Config ===
# Loading the Gemini model key from the .env (To access Google Gemini Model) 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Endpoint for generating the embedding with gemini embedding-001 model
EMBEDDING_URL = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent"

# Endpoint for generating chat response from the retrieved chunks with google gemini-2.0-flash model
CHAT_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# === ChromaDB Config ===
# Defining collection name to store document embeddings in chroma db
CHROMADB_COLLECTION = "documents"

# === Upload Config ===
# Directory for storing uploaded file in he disk
UPLOAD_FOLDER = "uploads/"

# Allowed file extention for file upload 
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

# Maximum file size allowed to be uploaded 
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

# === Logging Config ===
# Log file path to store the logs in the file 
LOG_FILE = "app.log"

# === Auth ===
# Admin credential for Authentication 
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# === Flask Secret Key ===
# Secret Key for flask session and CSRF Protection
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")