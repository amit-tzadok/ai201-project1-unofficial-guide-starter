"""
Embedding and retrieval module.

Embeds chunks using all-MiniLM-L6-v2, stores them in ChromaDB,
and provides semantic search over the collection.
"""

import chromadb
from sentence_transformers import SentenceTransformer
from ingest import ingest_all


# Load embedding model (runs locally, no API key needed)
_model = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB persistent storage
_client = chromadb.PersistentClient(path="./chroma_db")


def build_vector_store(collection_name="ub_cs_guide"):
    """Embed all chunks and store them in ChromaDB.

    Deletes existing collection if it exists and rebuilds from scratch.
    Returns the collection and the number of chunks stored.
    """
    # Delete existing collection if it exists
    existing = [c.name for c in _client.list_collections()]
    if collection_name in existing:
        _client.delete_collection(collection_name)

    collection = _client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}  # use cosine similarity
    )

    # Load and chunk all documents
    chunks = ingest_all()

    # Prepare data for ChromaDB
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [{"source": chunk["source"]} for chunk in chunks]

    # Embed all chunks
    embeddings = _model.encode(documents, show_progress_bar=True).tolist()

    # Add to collection
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    return collection, len(chunks)


def retrieve(query, k=5, collection_name="ub_cs_guide"):
    """Retrieve the top-k most relevant chunks for a query.

    Returns a list of dicts:
    [{"text": "...", "source": "...", "distance": 0.xx}]
    """
    collection = _client.get_collection(
        name=collection_name,
    )

    # Embed the query
    query_embedding = _model.encode([query]).tolist()

    # Search
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
    )

    # Format results
    retrieved = []
    for i in range(len(results["documents"][0])):
        retrieved.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i],
        })

    return retrieved


if __name__ == "__main__":
    import sys

    # Build the vector store
    print("Building vector store...")
    collection, count = build_vector_store()
    print(f"Stored {count} chunks in ChromaDB.\n")

    # Test with evaluation plan queries
    test_queries = [
        "When should I start leetcoding and what should I focus on first?",
        "Which CS clubs should I join as a freshman?",
        "How do I prepare for the STEAM career fair?",
    ]

    for query in test_queries:
        print(f"Query: {query}")
        print("-" * 60)
        results = retrieve(query)
        for i, r in enumerate(results, 1):
            print(f"  #{i} (distance: {r['distance']:.4f}) [{r['source']}]")
            # Show first 150 chars of the chunk
            preview = r["text"][:150].replace("\n", " ")
            print(f"     {preview}...")
        print()
