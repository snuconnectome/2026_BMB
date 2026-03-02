import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from data_loader import load_syllabus_excel, load_text_document
from langchain_text_splitters import RecursiveCharacterTextSplitter

DB_PATH = "/Users/jiookcha/Documents/git/2026_BMB/data/vector_store/bmb_index"

def build_vector_db():
    print("Initializing Embeddings (HuggingFace all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print("Loading documents...")
    # Adjust paths relative to the project root
    syllabus_docs = load_syllabus_excel("/Users/jiookcha/Documents/git/2026_BMB/2026시간표.xlsx")
    plan_docs = load_text_document("/Users/jiookcha/.gemini/antigravity/brain/775687b4-5e5a-4ca6-9b57-77ba50c2fb02/master_plan.md")
    all_docs = syllabus_docs + plan_docs

    if not all_docs:
        print("No documents loaded. Exiting.")
        return

    print(f"Splitting {len(all_docs)} documents...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = text_splitter.split_documents(all_docs)

    print(f"Building FAISS vector store with {len(split_docs)} chunks...")
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    print(f"Saving vector store to {DB_PATH}...")
    vectorstore.save_local(DB_PATH)
    print("Done! Vector database built successfully.")

if __name__ == "__main__":
    build_vector_db()
