from flask import Flask, send_from_directory
import logging
from config import LOG_FILE, UPLOAD_FOLDER, MAX_CONTENT_LENGTH, FLASK_SECRET_KEY
from app.routes.upload import upload_bp
from app.routes.home import home_bp
from app.routes.chat import chat_bp

# Initialize the Flask application with custom template and static folders
app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

# Set secret key for session management and security
app.secret_key = FLASK_SECRET_KEY

# Configure upload folder and maximum content size (e.g., for file uploads)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Logging setup
# Logs will be written both to a file and the console with INFO level
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Create a logger for this module
logger = logging.getLogger(__name__)

# Register Blueprints for modular route organization
app.register_blueprint(upload_bp)   # Handles upload-related routes
app.register_blueprint(home_bp)     # Handles home page or general UI routes
app.register_blueprint(chat_bp)     # Handles chat-related routes

# Serve the frontend in the root route 
@app.route('/')
def serve_frontend():
    logger.info("Serving frontend UI.")
    return send_from_directory("app/templates", "index.html")

# Serve the index if wrong route is hit 
@app.errorhandler(404)
def not_found(e):
    return send_from_directory("app/templates", "index.html")

if __name__ == "__main__":
    # Start the flask development Server.
    logger.info("Starting Flask server...")
    app.run(debug=True)
