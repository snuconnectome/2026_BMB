import os
import sys

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from qdrant_client import QdrantClient

# Set up paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QDRANT_PATH = os.path.join(BASE_DIR, "data", "vector_store", "qdrant_db")
COLLECTION_NAME = "bmb_2026_hybrid"

def run_local_rag_demo():
    print("==================================================")
    print(" 🧠 Local Mac RAG Demo (Zero API Cost, Millisecond latency) 🧠")
    print("==================================================")
    
    # 1. Initialize the same embeddings used in DGX-Spark
    print("[1/3] Loading Embeddings into Mac memory...")
    dense_embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
    
    # 2. Connect to the local Qdrant Database folder we downloaded
    print(f"[2/3] Connecting to Local offline DB at: {QDRANT_PATH}")
    qdrant = QdrantVectorStore.from_existing_collection(
        embedding=dense_embeddings,
        sparse_embedding=sparse_embeddings,
        retrieval_mode=RetrievalMode.HYBRID,
        path=QDRANT_PATH,
        collection_name=COLLECTION_NAME,
    )
    
    # Create an optimized retriever
    # search_type="similarity" is standard, "mmr" tries to fetch diverse documents
    retriever = qdrant.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    
    # 3. Perform a lightning-fast local search!
    # You can change this question to anything related to the syllabus or master plan
    query = "강의계획서에서 첫 수업(오리엔테이션)의 주요 내용이 무엇인가요?"
    print(f"\n[3/3] Executing Query: '{query}'\n")
    
    results = retriever.invoke(query)
    
    print("🔍 TOP 3 SEARCH RESULTS 🔍")
    for i, doc in enumerate(results, 1):
        print(f"\n--- Result #{i} (Score: {doc.metadata.get('_score', 'N/A')}) ---")
        source = os.path.basename(doc.metadata.get('source', 'Unknown'))
        print(f"📄 Source File: {source}")
        
        # Print a snippet of the content
        content = doc.page_content.replace('\n', ' ').strip()
        print(f"💬 Content Snippet: {content[:200]}..." if len(content) > 200 else f"💬 Content: {content}")

if __name__ == "__main__":
    run_local_rag_demo()
