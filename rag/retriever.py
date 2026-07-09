import chromadb
from sentence_transformers import SentenceTransformer

# Global model variable
model = None


def get_model():
    """
    Load the embedding model only when needed.
    """
    global model

    if model is None:
        print("Loading retrieval embedding model...")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Retrieval embedding model loaded.")

    return model


# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="legal_documents"
)


def retrieve_chunks(query, top_k=5):
    """
    Retrieve relevant document chunks along with IDs.
    """

    embedding_model = get_model()

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return {
        "documents": results["documents"][0],
        "ids": results["ids"][0]
    }