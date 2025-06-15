from flask import Flask, send_from_directory
import logging
from config import LOG_FILE, UPLOAD_FOLDER, MAX_CONTENT_LENGTH
from app.routes.upload import upload_bp
from app.routes.home import home_bp
from app.routes.chat import chat_bp

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)
app.secret_key = "your-secret-key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Register blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(home_bp)
app.register_blueprint(chat_bp)


@app.route('/')
def serve_frontend():
    logger.info("Serving frontend UI.")
    return send_from_directory("app/templates", "index.html")

@app.errorhandler(404)
def not_found(e):
    return send_from_directory("app/templates", "index.html")

if __name__ == "__main__":
    logger.info("Starting Flask server...")
    app.run(debug=True)
