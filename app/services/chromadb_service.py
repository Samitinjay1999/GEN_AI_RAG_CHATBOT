import chromadb
import uuid
import logging
from config import CHROMADB_COLLECTION

logger = logging.getLogger(__name__)

# === Initialize local ChromaDB client ===
client = chromadb.PersistentClient(path="./chroma_store")

# Create or get collection
collection = client.get_or_create_collection(CHROMADB_COLLECTION)


# === Add chunks to ChromaDB ===
def add_documents(chunks, embeddings, file_id):
    try:
        ids = [str(uuid.uuid4()) for _ in chunks]
        metadata = [{"file_id": file_id, "chunk_index": i} for i in range(len(chunks))]

        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadata
        )
        logger.info(f"Inserted {len(chunks)} chunks into ChromaDB.")
    except Exception as e:
        logger.error(f"Failed to add to ChromaDB: {e}")

# === Query relevant chunks from ChromaDB ===
def query_chunks(query_embedding, top_k=5):
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        logger.info(f"ChromaDB returned {len(results['documents'][0])} relevant chunks.")
        return results["documents"][0]
    except Exception as e:
        logger.error(f"ChromaDB query failed: {e}")
        return []
