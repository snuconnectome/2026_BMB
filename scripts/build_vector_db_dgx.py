import os
import argparse
import multiprocessing
from functools import partial
from typing import List

import torch
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_loader import load_syllabus_excel, load_text_document

# Resolve paths relative to the current script's directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "vector_store", "bmb_index_dgx")

def process_document(doc: Document) -> List[Document]:
    """
    Apply semantic chunking individually to a document.
    This function is run by worker processes.
    """
    source = doc.metadata.get("source", "")
    
    if source.endswith(".md"):
        # Semantic chunking for markdown files
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        splits = markdown_splitter.split_text(doc.page_content)
        # Preserve original metadata
        for split in splits:
            split.metadata.update(doc.metadata)
        return splits
        
    elif source.endswith(".xlsx"):
        # Excel rows are already conceptually chunked by Data Loader into meaningful rows.
        # But if they are too long, simply split them textually 
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return text_splitter.split_documents([doc])
        
    else:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return text_splitter.split_documents([doc])


def build_vector_db_dgx(batch_size: int, num_workers: int):
    print("=" * 50)
    print("🚀 DGX-Spark Optimized Vector DB Ingestion Pipeline 🚀")
    print("=" * 50)
    
    # Check GPU availability
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda":
        num_gpus = torch.cuda.device_count()
        print(f"[INFO] Using {num_gpus} GPU(s) for embeddings.")
    else:
        print("[WARNING] CUDA not available. Running on CPU (Expected to be slow).")

    print(f"[INFO] Initializing Embeddings (HuggingFace all-MiniLM-L6-v2) on {device}...")
    # NOTE: For true 2026 SOTA, we would swap out all-MiniLM for OpenAI API or a high-res embedding model here
    # Since we're running locally/DGX, we set the encode kwargs to use batching
    encode_kwargs = {'batch_size': batch_size}
    if device == "cuda":
        encode_kwargs['device'] = 'cuda'
        
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2", 
        model_kwargs={'device': device},
        encode_kwargs=encode_kwargs
    )
    
    print("[INFO] Loading raw documents into memory...")
    # Adjust paths relative to the project root
    syllabus_docs = load_syllabus_excel(os.path.join(BASE_DIR, "2026시간표.xlsx"))
    
    # We will try to load the master plan. Note: using the same absolute path as prototype
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
    # Multiprocessing for semantic chunking
    with multiprocessing.Pool(processes=num_workers) as pool:
        # map returns a list of lists of documents
        results = pool.map(process_document, all_raw_docs)
        for sublist in results:
            split_docs.extend(sublist)
            
    print(f"[INFO] Created {len(split_docs)} semantic chunks.")

    print(f"[INFO] Batch Embedding & Building FAISS Vector Store...")
    # FAISS from_documents internally calls embeddings.embed_documents, 
    # which we configured to use GPU and batching above.
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    print(f"[INFO] Saving vector store to {DB_PATH}...")
    vectorstore.save_local(DB_PATH)
    print("✅ Done! GPU-accelerated Vector Database built successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Vector DB using DGX GPU & Multiprocessing")
    parser.add_argument("--batch-size", type=int, default=256, help="GPU Embedding Batch Size")
    parser.add_argument("--workers", type=int, default=max(1, multiprocessing.cpu_count() - 1), help="Number of CPU workers for parsing")
    
    args = parser.parse_args()
    build_vector_db_dgx(args.batch_size, args.workers)
