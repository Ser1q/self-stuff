import chromadb

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_collection")

collection.upsert(
    ids=["id1", "id2"],
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ]
)

results = collection.query(
    query_texts=["Hawaii has great fruits."],
    n_results=2
)

print(results)