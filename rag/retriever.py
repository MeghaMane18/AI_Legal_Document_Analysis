import chromadb

# Import the same embedding model used during indexing
from rag.embeddings import get_model

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="legal_documents"
)


def retrieve_chunks(query, top_k=5):
    """
    Retrieve the most relevant document chunks.
    """

    embedding_model = get_model()

    query_embedding = embedding_model.encode(
        query,
        show_progress_bar=False
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return {
        "documents": results.get("documents", [[]])[0],
        "ids": results.get("ids", [[]])[0]
    }