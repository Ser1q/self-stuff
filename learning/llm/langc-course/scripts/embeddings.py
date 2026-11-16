from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import numpy as np

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def basic_embedding():
    query = "What is Machine Learning?"
    
    singe_embedding = embeddings.embed_query(query)
    print(len(singe_embedding)) # vector dimensions
    print(singe_embedding[:5]) # first 5 values
    print(np.linalg.norm(singe_embedding)) # vector norm
    
def batch_embedding():
    text = [
        "What is Langchain?",
        "What is Deep Learning?",
        "What are differences of Machine Learning and Deep Learning?"
    ]
    
    batch_emb = embeddings.embed_documents(text)
    
    for i, emb in enumerate(batch_emb):
        print(f"Text {i+1} - Vector dimensions: {len(emb)}")
        print (f"Text {i+1} - First 5 values: {emb[:5]}") 
        print (f"Text {i+1} - Vector norm: {np.linalg.norm(emb):.4f}")

def similarity_search():
    docs = [
        "Python is a programming language",
        "JavaScript is used for web development",
        "Machine learning enables AI applications",
        "Deep learning uses neural networks",
        "Cats are popular pets",
    ]
    
    query = "What programming languages exists?"
    
    doc_vectors = embeddings.embed_documents(docs)
    query_vector = embeddings.embed_query(query)
    
    def cosine_distance(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    similarity = [cosine_distance(query_vector, doc_vec) for doc_vec in doc_vectors]
    
    ranked_docs = sorted(zip(docs, similarity), key=lambda x: x[1], reverse=True)
    
    print(f"Query: {query}\n")
    print("Ranked by similarity:")
    for doc, score in ranked_docs:
        print(f"  {score:.4f}: {doc}")

if __name__ == "__main__":
    # basic_embedding()
    # batch_embedding()
    similarity_search()