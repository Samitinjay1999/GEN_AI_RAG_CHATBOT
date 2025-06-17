import os
import uuid
import logging
from flask import Blueprint, request, session, jsonify
from werkzeug.utils import secure_filename
from app.routes.home import login_required
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from app.services.utils import clean_text, read_pdf, read_txt, chunk_text
from app.services.embedding import get_embedding
from app.services.chromadb_service import add_documents

# logger setut
logger = logging.getLogger(__name__)

# define blueprint for upload route
upload_bp = Blueprint('upload', __name__)

# === Check if file extension is allowed ===
def allowed_file(filename):
    """
    Checks wheather the file contains . at first in the filename  
    Then checks if the file contains .pdf or .txt at the end or not 
    And returns boolean
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# === Upload endpoint (POST only) ===
@upload_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """
    Handles file upload, processing, embedding, and storage in ChromaDB.
    Requires user to be logged in.
    - Accepts only PDF and TXT files.
    - Extracts and cleans text from uploaded document.
    - Splits the text into chunks.
    - Generates embeddings for each chunk.
    - Stores the chunks and their embeddings in ChromaDB.
    """
    if 'file' not in request.files:
        logger.warning("Upload failed: No file part in request")
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == '':
        logger.warning("Upload failed: No selected file")
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Save the file with unique uuid prefix
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())
        saved_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{filename}")
        file.save(saved_path)
        logger.info(f"File uploaded successfully: {filename} saved as {saved_path}")

        # === Process the file ===
        ext = os.path.splitext(saved_path)[1].lower()
        if ext == '.pdf':
            raw_text = read_pdf(saved_path) # Read the pdf and extract raw text
        elif ext == '.txt':
            raw_text = read_txt(saved_path) # Read the txt and extract raw text
        else:
            logger.warning("Unsupported file type.")
            return jsonify({"error": "Unsupported file type."}), 400
        
        # Clean the text 
        cleaned = clean_text(raw_text)
        logger.info(f"Extracted text length: {len(cleaned)}")

        # Split the cleaned texts into chunks 
        chunks = chunk_text(cleaned)
        logger.info(f"Generated {len(chunks)} chunks from document.")

        # Generate Embeddings of chunks
        embeddings = []
        for i, chunk in enumerate(chunks):
            emb = get_embedding(chunk)
            if emb:
                embeddings.append(emb)
            else:
                logger.warning(f"Failed to embed chunk {i}")
        
        # Save embeddings to chroma db
        if embeddings:
            add_documents(chunks, embeddings, unique_id)
            logger.info(f"Inserted {len(embeddings)} chunks into ChromaDB.")
        else:
            logger.warning("No embeddings generated; skipping ChromaDB insert.")
            return jsonify({"error": "No embeddings generated"}), 500


        # Return response if the file is uploaded succefully
        return jsonify({
            "message": "File uploaded and processed successfully.",
            "chunks": len(chunks),
            "file_id": unique_id
        }), 200

    else:
        logger.warning(f"Invalid file type attempted: {file.filename}")
        return jsonify({"error": "Invalid file type. Only PDF and TXT allowed."}), 400
