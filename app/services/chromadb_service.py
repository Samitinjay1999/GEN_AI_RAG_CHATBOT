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
    """
    Adds text chunks with their embeddings into ChromaDB.

    Args:
        chunks (List[str]): List of document text chunks.
        embeddings (List[List[float]]): Corresponding embedding vectors.
        file_id (str): Unique file ID to associate chunks for later filtering or grouping.

    Returns:
        None
    """
    try:
        # Generate a unique ching UUID for each chunk
        ids = [str(uuid.uuid4()) for _ in chunks]
        # Add meta data for traceability
        metadata = [{"file_id": file_id, "chunk_index": i} for i in range(len(chunks))]
        # Add data to the Chroma db
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
    """
    Retrieves the most relevant chunks from ChromaDB using a query embedding.

    Args:
        query_embedding (List[float]): Embedding of the user query.
        top_k (int): Number of top similar results to return.

    Returns:
        List[str]: List of most relevant document chunks (or empty list on failure).
    """
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
