# Chunking - Makes or Breaks RAG
Chunking is not preprocessing, it's ARCHITECTURE

## Fixed chunking
Chunk can be split right in the middle of the sentence, since it is limited by ex. 500 chars for each chunk.
Meaning is split across two distinct chunks, so when search neither of chunks have complete answer

## Semantic Chunking 
Chunk is split in the meaning boundaries, with complete sections and answers.

Each chunk is embedded in isolation into the model, so bad chunking will result in incomplete context 
for the model. The model sees only fragments, not the whole concept

## Chunking Variables
1) Chunk Size
- Too small -> loses context
- Too large -> dilutes meaning, lost tokens
Sweet spot is about 200 - 1000 tokens

2) Overlap
10 - 20% overlap preserves context between the chunks, so they are not too fragmented, else they would lose 
context of eachother's relation

3) Split Boundaries
- Fixed (Random Cut)
- Recursive (cutting and paragraphs/sentences)
- Semantic (cutting at meaning boundaries) (best) 

4) Content Type
Ex. code, legal, markdown
Each needs different treatment

# Chunking Strategies Compared
## Fixed-Size Chunking - How It Works And Why Is't Bad

How it works:
- It cuts at exact intervals (ex. 500 chars)

The problematic results:
- mid word cut (incomplete chunks)
- no context (fragments)
- too small (useless)

Pros:
- Simple implementations
- Fast processing
- Predictalbe chunk sizes

Cons:
- Destroys meaning
- Inaccurate retertieval
- Poor quality results
- Frustrating user experience

Use case -> simple and fast prototypes or very specific contraints ONLY 

NOT FOR PRODUCTION!

## Recursive Chunking - The Reliable Default
It respects natural boundaries

Paragraph (\\n\\n) (if too big) -> Lines (\\n) (if too big) -> Sentences (.) (if still too big) -> Clauses (,) (if still too big) -> Words (`) -> Characters (last resort)

Good balance of quality + speed 

80% of production uses Recursive Chunking 

Recommended Refault (Langchain uses it)

## Semantic Chunking - Best Quality
Splitting at meaning boundaries, not structure or some arbitrary points.

1) Embed each sentence
2) Compare adjacent embeddings
3) Split when the similarity drops

Chunk 1: [S1, S2, S3] -> OAuth Topic
Chunk 2: [S4, S5, S6] -> Rate Limit Topic

The premium option if the best quality is needed (legal documents, technical manuals, knowledge basees etc.). Used when Accuracy > Speed. Speed is slow

| Sentence ID | Similarity Score |
|:-----------:|:----------------:|
| **s1**      | 9                |
| **s2**      | 8                |
| **s3**      | 9                |
| **s4**      | 2                |
| **s5**      | 9                |
| **s6**      | 9                |
| **s7**      | 8                |

```mermaid
xyChart-beta
    title: Sentence Similarity Scores
    x-axis: Sentences [s1, s2, s3, s4, s5, s6, s7]
    y-axis: Similarity Score (0-10)
    bar1: [9, 8, 9, 2, 9, 9, 8]
    line1: [9, 8, 9, 2, 9, 9, 8]
    color1: #4E79A7
    color2: #F28E2B
```

## Late Chunking - The Future of Chunking

Traditional Chunking - document is first splitted into chunks and only then embedded. The chunks are isolated and Chunk 5 for example has NO IDEA about what chunks 1 - 4 contain. It loses cross chunk context.

Late Chunking - document is first EMBEDDED and ony then splitted into chunks, so context is preserver regarding full document and chunks know about each other. Chunk 5 embedding includes FULL DOCUMENT CONTEXT. It results in 10 - 12% accuracy improvement

Cutting edge however is that it requires specific model support.
Models: jina-embeddings-v2 etc.

# The 5 RAG Failure Models

## 1) Bad Chunking

Disjoint context, so the chunks individually mean no sense when given to llm.

Overlapping ensures the preservance of context between chunks, so for example the previous sentences partial information, still present in the next chunk, and the context is preserved accordingly.

Without overlap:
Chunk 1 end: ...er the lazy dog. The Chunk 2 start: quick brown fox jump...
With overlap:
Chunk 1 end: ...er the lazy dog. The Chunk 2 start: the lazy dog. The qu...

Overlap is cheap ensurance, that the content between the chunks isn't orphaned.


## 2) Embedding Mismatch - users query vector incorrectly mathced with document's vector

When users use the different words from the ones present in document, the semantic search fails.

Embedding is turning the query into the vector, so the computer can understand its content and compare it with the vectors of documents and find similar. 
Normalizing the vector prevents bigger documents/queries having more value than the small documents/queries. It is set to 1. Norm is basically measuring the magnitude of a vector.

3) Retrieval Noise
4) Context Overflow 
5) Hallucination


