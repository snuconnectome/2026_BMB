import pandas as pd
import os
from typing import Dict

def evaluate_etl_contributions(csv_path: str) -> Dict[str, dict]:
    """
    Parses a CSV export of the SNU eTL forum to evaluate the 1-2-1 Rule:
    - 1 Post (Self submission)
    - 2 Attacks (Replies to others)
    - 1 Defense (Replies to comments on your post)
    
    Returns a dictionary of student_id -> evaluation metrics.
    """
    if not os.path.exists(csv_path):
        print(f"eTL Data File not found: {csv_path}")
        return {}

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading eTL data: {e}")
        return {}
        
    # Assuming standard eTL forum dump columns for demonstration:
    # 'Student_ID', 'Post_Type' (Thread, Reply), 'Parent_Thread_Author_ID'
    
    eval_results = {}
    
    for student_id in df['Student_ID'].unique():
        student_data = df[df['Student_ID'] == student_id]
        
        # 1. Count original threads -> Post requirement
        original_threads = len(student_data[student_data['Post_Type'] == 'Thread'])
        
        # 2. Count replies to others -> Attack requirement
        replies_to_others = len(student_data[(student_data['Post_Type'] == 'Reply') & (student_data['Parent_Thread_Author_ID'] != student_id)])
        
        # 3. Count replies to their own threads -> Defense requirement
        defenses = len(student_data[(student_data['Post_Type'] == 'Reply') & (student_data['Parent_Thread_Author_ID'] == student_id)])
        
        eval_results[student_id] = {
            "posts": original_threads,
            "attacks": replies_to_others,
            "defenses": defenses,
            "passed_121_rule": (original_threads >= 1 and replies_to_others >= 2 and defenses >= 1)
        }
        
    return eval_results

if __name__ == "__main__":
    print("eTL Contribution Evaluator loaded.")
