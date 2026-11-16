from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter,
    Language
)
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

# Sample documents for testing
SAMPLE_TEXT = """# Introduction to Machine Learning

Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.

## Types of Machine Learning

### Supervised Learning
Supervised learning uses labeled data to train models. The algorithm learns to map inputs to outputs based on example input-output pairs.

Common algorithms include:
- Linear Regression
- Decision Trees
- Neural Networks

### Unsupervised Learning
Unsupervised learning finds hidden patterns in unlabeled data. The algorithm discovers structure without predefined labels.

Common algorithms include:
- K-Means Clustering
- Principal Component Analysis
- Autoencoders

## Applications

Machine learning is used in many fields:
1. Image recognition
2. Natural language processing
3. Recommendation systems
4. Fraud detection
5. Autonomous vehicles
""".strip()

SAMPLE_CODE = '''
def quicksort(arr):
    """
    Quicksort implementation in Python.
    Time complexity: O(n log n) average, O(n²) worst case.
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quicksort(left) + middle + quicksort(right)


def binary_search(arr, target):
    """
    Binary search implementation.
    Requires sorted array.
    Time complexity: O(log n)
    """
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
'''


def recursive_text_splitter():
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", "," " ", ""])
    
    chunks = splitter.split_text(SAMPLE_TEXT)
    
    print(f"Original length: {len(SAMPLE_TEXT)}")
    print(f"Chunks number: {len(chunks)}")
    print(f"Chunk Sizes: {[len(c) for c in chunks]}")
    print(f"Chunk preview: {chunks[0][:100]}")
    
    
def markdown_splitter():
    headers = [
        ("#", "h1"),
        ("##", "h2"),
        ("###", "h3")
    ]
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers)
    
    chunks = splitter.split_text(SAMPLE_TEXT) # returns documents btw
    
    print(f"Markdown Splitter produced {len(chunks)} chunks.")
    
    for i, chunk in enumerate(chunks):
        print(f"--- Chunk {i+1} ---")
        print(f" Metadata: {chunk.metadata}\n")
        print(f" Content: {chunk.page_content[:200]}...\n")
    
def code_splitter():
    python_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, 
        chunk_size=500,
        chunk_overlap=50
    )
    
    chunks = python_splitter.split_text(SAMPLE_CODE)
    
    print(f"Original length: {len(SAMPLE_TEXT)}")
    print(f"Chunks number: {len(chunks)}")
    print(f"Chunk Sizes: {[len(c) for c in chunks]}")
    print(f"Chunk 1 preview: {chunks[0][:100]}")
    print(f"Chunk 2 preview: {chunks[1][:100]}")

def document_splitter():
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_core.documents import Document
    
    loader = PyPDFLoader("./docs/sql_course.pdf")
    docs = loader.load()
    
    print(f"Loaded {len(docs)} documents")
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    chunks = splitter.split_documents(docs)
    
    print(f"Split into {len(chunks)} chunks")
    print(f"\nFirst chunk metadata: {chunks[0].metadata}")
    print(f"First chunk content: {chunks[0].page_content[:200]}...")
    print(f"\nLast chunk metadata: {chunks[-1].metadata}")
    
if __name__ == "__main__":
    # recursive_text_splitter()
    # markdown_splitter() 
    # code_splitter()
    document_splitter()

