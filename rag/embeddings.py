from sentence_transformers import SentenceTransformer

# Global model variable
model = None


def get_model():
    """
    Load the embedding model only when needed.
    """
    global model

    if model is None:
        print("Loading embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Embedding model loaded.")

    return model


def create_embeddings(chunks):
    """
    Convert text chunks into vector embeddings.
    """
    embedding_model = get_model()

    embeddings = embedding_model.encode(chunks)

    return embeddings