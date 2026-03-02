import os
import sys
import argparse
import multiprocessing
from typing import List

from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore, FastEmbedSparse, RetrievalMode
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter

# Load environment variables from .env file
load_dotenv()

# Ensure local data_loader can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import load_syllabus_excel, load_text_document

# Resolve paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QDRANT_PATH = os.path.join(BASE_DIR, "data", "vector_store", "qdrant_db")
COLLECTION_NAME = "bmb_2026_hybrid"

def process_document(doc: Document) -> List[Document]:
    """
    Apply semantic chunking individually to a document.
    """
    source = doc.metadata.get("source", "")
    
    if source.endswith(".md"):
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        splits = markdown_splitter.split_text(doc.page_content)
        for split in splits:
            split.metadata.update(doc.metadata)
        return splits
        
    else:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return text_splitter.split_documents([doc])


def build_qdrant_hybrid_db(num_workers: int):
    print("=" * 60)
    print("🚀 DGX-Spark Hybrid Vector DB Ingestion (Qdrant + Gemini) 🚀")
    print("=" * 60)
    
    print("[INFO] Initializing High-Res Embeddings (HuggingFace BAAI/bge-small-en-v1.5)...")
    dense_embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    print("[INFO] Initializing Sparse Embeddings (FastEmbed BM25)...")
    sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")

    print("[INFO] Loading raw documents into memory...")
    syllabus_docs = load_syllabus_excel(os.path.join(BASE_DIR, "2026시간표.xlsx"))
    
    master_plan_path = os.path.join(BASE_DIR, "bmb_course_brainstorming_chat_log.md")
    try:
        plan_docs = load_text_document(master_plan_path)
    except Exception as e:
        print(f"[WARNING] Could not load master plan: {e}")
        plan_docs = []
        
    all_raw_docs = syllabus_docs + plan_docs

    if not all_raw_docs:
        print("[ERROR] No documents loaded. Exiting.")
        return

    print(f"[INFO] Total Raw Documents: {len(all_raw_docs)}")
    print(f"[INFO] Starting parallel Semantic Chunking with {num_workers} workers...")
    
    split_docs = []
    with multiprocessing.Pool(processes=num_workers) as pool:
        results = pool.map(process_document, all_raw_docs)
        for sublist in results:
            split_docs.extend(sublist)
            
    print(f"[INFO] Created {len(split_docs)} semantic chunks.")

    print(f"[INFO] Building Qdrant Hybrid Vector Store at {QDRANT_PATH}...")
    
    # Ensure directory exists
    os.makedirs(QDRANT_PATH, exist_ok=True)
    
    # We use QdrantVectorStore from langchain_qdrant
    qdrant = QdrantVectorStore.from_documents(
        split_docs,
        embedding=dense_embeddings,
        sparse_embedding=sparse_embeddings,
        retrieval_mode=RetrievalMode.HYBRID,
        path=QDRANT_PATH,
        collection_name=COLLECTION_NAME,
        force_recreate=True
    )

    print(f"✅ Done! Hybrid Vector Database built successfully at {QDRANT_PATH}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Hybrid Vector DB using Qdrant")
    parser.add_argument("--workers", type=int, default=max(1, multiprocessing.cpu_count() - 1), help="Number of CPU workers for parsing")
    
    args = parser.parse_args()
    build_qdrant_hybrid_db(args.workers)
