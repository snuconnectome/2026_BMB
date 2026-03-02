import os
import re
from notion_client import Client

# Initialize Notion Client
# Requires NOTION_TOKEN in environment variables
notion = Client(auth=os.getenv("NOTION_TOKEN"))

TARGET_PAGE_ID = "31741454561d80fb9efdc4487b1df2c2"

def create_child_page(parent_id, title):
    """Creates a new child page under the specified parent."""
    new_page = notion.pages.create(
        parent={"page_id": parent_id},
        properties={
            "title": {
                "title": [{"text": {"content": title}}]
            }
        }
    )
    return new_page["id"]

def split_markdown_into_blocks(markdown_text):
    """
    Very basic markdown to Notion block converter.
    For a production script, a robust markdown-to-notion library is recommended.
    This handles basic headers and paragraphs.
    """
    blocks = []
    lines = markdown_text.split('\n')
    
    current_paragraph = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_paragraph:
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": " ".join(current_paragraph)}}]
                    }
                })
                current_paragraph = []
            continue
            
        if line.startswith('# '):
            blocks.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}
            })
        elif line.startswith('## '):
            blocks.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": line[3:]}}]}
            })
        elif line.startswith('### '):
            blocks.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": line[4:]}}]}
            })
        elif line.startswith('- ') or line.startswith('* '):
             blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": line[2:]}}]}
            })
        else:
            # Strip simple markdown for plain text upload if needed, or just append
            clean_line = re.sub(r'[*_`]', '', line) 
            current_paragraph.append(clean_line)
            
    if current_paragraph:
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": " ".join(current_paragraph)}}]
            }
        })
        
    return blocks

def upload_markdown_file(file_path, parent_page_id, page_title):
    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"Creating page '{page_title}' in Notion...")
    new_page_id = create_child_page(parent_page_id, page_title)
    
    print(f"Parsing markdown into blocks...")
    blocks = split_markdown_into_blocks(content)
    
    print(f"Uploading {len(blocks)} blocks to Notion...")
    # Notion API limits block appends to 100 per request
    chunk_size = 100
    for i in range(0, len(blocks), chunk_size):
        chunk = blocks[i:i + chunk_size]
        notion.blocks.children.append(
            block_id=new_page_id,
            children=chunk
        )
    print("Done!")

if __name__ == "__main__":
    docs_to_sync = [
        {"path": "/Users/jiookcha/Documents/git/2026_BMB/docs/syllabus/syllabus_2026_agentic.md", "title": "2026 BMB Syllabus (Agentic)"},
        {"path": "/Users/jiookcha/Documents/git/2026_BMB/docs/hybrid_orchestration_guide.md", "title": "Hybrid Orchestration Guide"},
        {"path": "/Users/jiookcha/Documents/git/2026_BMB/docs/homework/bmb_self_observation_homework.md", "title": "BMB Self-Observation Homework"}
    ]
    
    for doc in docs_to_sync:
        if os.path.exists(doc["path"]):
            try:
                upload_markdown_file(doc["path"], TARGET_PAGE_ID, doc["title"])
            except Exception as e:
                print(f"Error uploading {doc['title']}: {e}")
        else:
            print(f"File not found: {doc['path']}")
