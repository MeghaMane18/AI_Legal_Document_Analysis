import chromadb

# Create Chroma client
client = chromadb.PersistentClient(path="chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="legal_documents"
)


def store_embeddings(chunks, embeddings):
    """
    Store chunks and embeddings in ChromaDB.
    """

    ids = [str(i) for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist()
    )

    print("Embeddings stored successfully in ChromaDB.")