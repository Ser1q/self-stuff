from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
)
from dotenv import load_dotenv

load_dotenv()

def load_text_file(text_path: str):
    loader = TextLoader(text_path)
    documents = loader.load()
    
    print(f"Loaded {len(documents)} document(s)")
    print(f"Content preview: {documents[0].page_content[:100]}...")
    print(f"Metadata: {documents[0].metadata}")
    
def pdf_loader(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    print(f"Loaded {len(documents)} document(s)")
    for i, doc in enumerate(documents):
        print(f"Document {i+1} Content Preview: {doc.page_content[:100]}")
        print(f"Metadata: {doc.metadata}")

if __name__ == "__main__":
    # load_text_file(./docs/tempfile.txt)  
    pdf_loader('./docs/sql_course.pdf')