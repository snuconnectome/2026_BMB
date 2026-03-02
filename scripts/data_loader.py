import os
import pandas as pd
from langchain_core.documents import Document

def load_syllabus_excel(file_path):
    """
    Loads the 2026 BMB Syllabus Excel file into LangChain Documents.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    
    # Read Excel, skipping empty rows at the top if any
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading Excel: {e}")
        return []

    docs = []
    # Identify key columns based on header index or name.
    # The actual columns based on our previous probe were like 'Unnamed: X', but visually: Date, Day, Prof, Dept, Topic...
    for i, row in df.iterrows():
        # Example extracting text from the row. We stringify all non-null values to capture the schedule item.
        row_dict = row.dropna().to_dict()
        if not row_dict:
            continue
        
        # We will create a rich text block combining all fields
        content_lines = []
        for k, v in row_dict.items():
             if str(v).strip():
                 content_lines.append(f"{k}: {v}")
        
        content = "\n".join(content_lines)
        if len(content) > 10: # Minimum meaningful content
            doc = Document(
                page_content=content,
                metadata={"source": file_path, "type": "syllabus_row", "row_index": i}
            )
            docs.append(doc)
            
    return docs

def load_text_document(file_path):
    """
    Load a pure text or markdown file into LangChain Documents.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Simple loading (we can add character level splitting later if needed)
    return [Document(page_content=content, metadata={"source": file_path, "type": "master_plan"})]

if __name__ == "__main__":
    docs1 = load_syllabus_excel("../2026시간표.xlsx")
    print(f"Loaded {len(docs1)} records from Syllabus Excel.")
    
    docs2 = load_text_document("/Users/jiookcha/.gemini/antigravity/brain/775687b4-5e5a-4ca6-9b57-77ba50c2fb02/master_plan.md")
    print(f"Loaded {len(docs2)} records from Master Plan.")
