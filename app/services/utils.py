import fitz  # PyMuPDF
import os
import re
import logging

logger = logging.getLogger(__name__)

# === Read PDF ===
def read_pdf(filepath):
    logger.info(f"Reading PDF: {filepath}")
    text = ""
    try:
        with fitz.open(filepath) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        logger.error(f"Failed to read PDF: {e}")
        return ""

# === Read TXT ===
def read_txt(filepath):
    logger.info(f"Reading TXT: {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logger.error(f"Failed to read TXT: {e}")
        return ""

# === Clean Text ===
def clean_text(text):
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# === Chunk Text into 200-word blocks ===
def chunk_text(text, chunk_size=200):
    logger.info(f"Chunking text into {chunk_size}-word blocks")
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        if chunk:
            chunks.append(chunk)

    logger.info(f"Total chunks created: {len(chunks)}")
    return chunks

# === Master: Process File and Return Chunks ===
def process_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    text = ""

    if ext == '.pdf':
        text = read_pdf(filepath)
    elif ext == '.txt':
        text = read_txt(filepath)
    else:
        logger.warning(f"Unsupported file type: {ext}")
        return []

    clean = clean_text(text)
    return chunk_text(clean)
