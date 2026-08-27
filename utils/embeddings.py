import numpy as np

# Lazy load to avoid slowing down app startup
_model = None

def get_embedding_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            # Using a very small and fast model for semantic search
            _model = SentenceTransformer("all-MiniLM-L6-v2")
        except ImportError:
            print("sentence-transformers not installed.")
            return None
    return _model

def get_embedding(text: str):
    model = get_embedding_model()
    if model is None:
        return None
    return model.encode(text)

def semantic_search(query: str, texts: list[str], top_k: int = 5):
    """
    Returns the indices of the top_k most similar texts to the query.
    """
    model = get_embedding_model()
    if model is None or not texts:
        return []
        
    try:
        from sklearn.metrics.pairwise import cosine_similarity
        query_embedding = model.encode([query])
        text_embeddings = model.encode(texts)
        
        similarities = cosine_similarity(query_embedding, text_embeddings)[0]
        # Get indices of top_k results, sorted by highest similarity
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        # Only return indices where similarity > a threshold (e.g., 0.1)
        valid_indices = [i for i in top_indices if similarities[i] > 0.1]
        return valid_indices
    except Exception as e:
        print(f"Error in semantic search: {e}")
        return []
