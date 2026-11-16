from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import tempfile

load_dotenv()

embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")

# Sample documents
SAMPLE_DOCS = [
    Document(
        page_content="LangChain is a framework for developing applications powered by language models.",
        metadata={"source": "langchain_docs", "topic": "overview"},
    ),
    Document(
        page_content="LangGraph is a library for building stateful, multi-actor applications with LLMs.",
        metadata={"source": "langgraph_docs", "topic": "overview"},
    ),
    Document(
        page_content="Vector stores are databases optimized for storing and searching embeddings.",
        metadata={"source": "vector_guide", "topic": "database"},
    ),
    Document(
        page_content="RAG combines retrieval with generation for more accurate LLM responses.",
        metadata={"source": "rag_guide", "topic": "architecture"},
    ),
    Document(
        page_content="Embeddings convert text into numerical vectors for semantic similarity.",
        metadata={"source": "embeddings_guide", "topic": "fundamentals"},
    ),
    Document(
        page_content="Chroma is an open-source embedding database for AI applications.",
        metadata={"source": "chroma_docs", "topic": "database"},
    ),
    Document(
        page_content="FAISS is a library for efficient similarity search developed by Facebook.",
        metadata={"source": "faiss_docs", "topic": "database"},
    ),
    Document(
        page_content="Pinecone is a managed vector database service for production workloads.",
        metadata={"source": "pinecone_docs", "topic": "database"},
    ),
]

Chroma.similarity_search

def similarity_search():
    with tempfile.TemporaryDirectory() as tmpdir:
        vectorstore = Chroma.from_documents(
            documents=SAMPLE_DOCS,
            embedding=embeddings_model,
            persist_directory=tmpdir
        )
        
        print(f"Documents in collection: {vectorstore._collection.count()}")
        
        query = "What is langchain"
        
        results = vectorstore.similarity_search(query=query, k=3)
        
        print(f"Top 3 results for query \"{query}\"")
        for i, doc in enumerate(results):
            print(f"Result {i+1}: {doc.page_content} (Source: {doc.metadata["source"]})")

def similarity_search_with_scores():
    with tempfile.TemporaryDirectory() as tmpdir:
        # create vector store from documents
        vectorstore = Chroma.from_documents(
            documents=SAMPLE_DOCS, embedding=embeddings_model, persist_directory=tmpdir
        )

        # perform similarity search with scores
        query = "Explain vector stores."
        results_with_scores = vectorstore.similarity_search_with_score(query, k=3)

        print(f"Top 3 results with scores for query '{query}':")
        
        for i, (doc, score) in enumerate(results_with_scores):
            print(f"Result {i+1}: {doc.page_content} (Distance: {score:.4f}, Source: {doc.metadata["source"]})")
                
        # for i, (doc, score) in enumerate(results_with_scores):
        #     final_score = 1 / (1 + score)  # Convert distance to similarity
        #     print(
        #         f"Result {i+1}: {doc.page_content} (Score: {final_score:.4f}, Source: {doc.metadata['source']})"
        #     )        

def metadata_filtering():
    with tempfile.TemporaryDirectory() as tmpdir:
        vectorstore = Chroma.from_documents(
            documents=SAMPLE_DOCS,
            embedding=embeddings_model,
            persist_directory=tmpdir
        )
        
        query = "What are available databases?"
        
        # Without filtering
        results = vectorstore.similarity_search(
            query=query, k=5
        )
        
        for i, doc in enumerate(results):
            print(f"Document {i+1}: {doc.page_content} (Source: {doc.metadata["source"]}, Topic: {doc.metadata["topic"]})")
        
        # With metadata filtering
        print(f"")
        filter_criteria = {"topic": "database"}
        
        filtered_results = vectorstore.similarity_search(
            query=query, k=5, filter=filter_criteria
        )
        
        for i, doc in enumerate(filtered_results):
            print(f"Document {i+1}: {doc.page_content} (Source: {doc.metadata["source"]}, Topic: {doc.metadata["topic"]})")
        
if __name__ == "__main__":
    # similarity_search()
    # similarity_search_with_scores()
    metadata_filtering()
