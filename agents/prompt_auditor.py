import os
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
# For testing locally without an API key we'll define a dummy model or prompt for you to hook up later.
# In production, use langchain_google_genai.ChatGoogleGenerativeAI or langchain_openai.ChatOpenAI

class PromptAuditScore(BaseModel):
    scientific_depth_score: int = Field(description="Score from 1 to 10 for scientific depth of questioning.")
    contradiction_identification_score: int = Field(description="Score from 1 to 10 for identifying logical flaws in literature.")
    strategic_ai_usage_score: int = Field(description="Score from 1 to 10 for strategic multi-turn AI control.")
    feedback: str = Field(description="Qualitative feedback explaining the scores and areas for improvement.")

def get_audit_prompt():
    system_prompt = """
    You are an AI-CoScientist evaluating an undergraduate student's 'Prompt Audit Report' in a Brain-Mind-Behavior neuroscience course.
    The goal of this course is NOT to memorize facts, but to learn how to ask AI the right questions, identify limitations in current literature, and design novel hypotheses.
    
    You will be provided with the student's multi-turn dialogue with an AI assistant.
    Evaluate the dialogue on three criteria (1-10 scale):
    1. Scientific Depth: Does the student ask deep mechanistically relevant questions about the brain and behavior?
    2. Contradiction Identification: Does the student push the AI to reveal logical contradictions or edge cases in existing papers?
    3. Strategic AI Usage: Is the student directing the AI like a CEO/CTO, rather than just asking for summarized answers (which is penalized)?
    
    Provide your evaluation strictly as structured output.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Student Multi-turn Dialogue:\n\n{dialogue}")
    ])
    
    return prompt

def evaluate_student_prompt_log(llm, dialogue_text: str) -> PromptAuditScore:
    """
    Evaluates a student's prompt report using the provided LLM.
    llm should be a structured output capable model (e.g., llm.with_structured_output(PromptAuditScore))
    """
    prompt = get_audit_prompt()
    chain = prompt | llm.with_structured_output(PromptAuditScore)
    
    result = chain.invoke({"dialogue": dialogue_text})
    return result

if __name__ == "__main__":
    print("Prompt Auditor module initialized. Ready to attach LLM.")
