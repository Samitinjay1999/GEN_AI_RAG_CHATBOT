import requests
import logging
from config import GEMINI_API_KEY, EMBEDDING_URL, CHAT_URL # Keep CHAT_URL as it's used in generate_gemini_response
import hashlib 

logger = logging.getLogger(__name__)

# === Embed a single chunk ===
def get_embedding(text):
    """
    Generates an embedding vector for a given text using the Gemini Embedding API.

    Args:
        text (str): The input text to embed.

    Returns:
        list or None: A list of embedding values if successful, else None.
    """
    try:
        # Use the EMBEDDING_URL from config.py
        url = f"{EMBEDDING_URL}?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {
            # Explicitly specifying the model is good practice for embeddingContent endpoint
            "model": "models/embedding-001",
            "content": {
                "parts": [
                    {"text": text}
                ]
            }
        }

        logger.debug(f"Sending embedding request to: {url}")
        logger.debug(f"Request data: {data}")

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() # Raise an exception if HTTP errors (4xx or 5xx)

        result = response.json()
        # For embedContent, the embedding values are typically under 'values'
        if "embedding" in result and "values" in result["embedding"]:
            return result["embedding"]["values"]
        else:
            logger.error(f"Embedding response missing 'embedding' or 'values' field: {result}")
            return None

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error during embedding: {http_err}")
        logger.error(f"Response status code: {http_err.response.status_code}")
        logger.error(f"Response text: {http_err.response.text}")
        return None
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Connection error during embedding: {conn_err}")
        return None
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Timeout error during embedding: {timeout_err}")
        return None
    except requests.exceptions.RequestException as req_err:
        logger.error(f"An error occurred during embedding request: {req_err}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred during embedding: {e}")
        # Try to log response text if available in case of a non-HTTP error after response
        if 'response' in locals() and response is not None:
            logger.error(f"Response text (if available): {response.text}")
        return None

def generate_gemini_response(prompt, context_chunks):
    """
    Uses the Gemini chat API to generate a natural language response using provided context chunks.

    Args:
        prompt (str): User query to be answered.
        context_chunks (list): Relevant document text chunks to provide context.

    Returns:
        str: Model-generated response or a fallback message on failure.
    """
    try:
        url = f"{CHAT_URL}?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}

        full_prompt = (
            "Use the following context to answer the user query.\n\n"
            "Context:\n" + "\n\n".join(context_chunks) + "\n\n"
            f"Query:\n{prompt}"
        )

        data = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": full_prompt}
                    ]
                }
            ]
        }
        
        logger.debug(f"Sending chat request to: {url}")
        logger.debug(f"Request data (first 200 chars of prompt): {full_prompt[:200]}...")

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        message = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        logger.info("Generated response from Gemini.")
        return message

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error during chat response generation: {http_err}")
        logger.error(f"Response status code: {http_err.response.status_code}")
        logger.error(f"Response text: {http_err.response.text}")
        return f"[ERROR] Failed to generate response due to HTTP error: {http_err.response.text if http_err.response else str(http_err)}"
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        logger.error(f"Response text: {response.text if 'response' in locals() else 'no response'}")
        return f"[MOCK] This is a placeholder response for: '{prompt}' using {len(context_chunks)} chunks. \n {context_chunks}"