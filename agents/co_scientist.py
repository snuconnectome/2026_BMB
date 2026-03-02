import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_coscientist_prompt():
    system_prompt = """
    You are an AI-CoScientist, an expert in Neuroscience, Cognitive Psychology, and Agentic AI.
    Your role is to simulate the 'The Pitch' phase of the Brain-Mind-Behavior class at Seoul National University.
    
    A student team has submitted a research hypothesis or a finding. You must act as the ultimate critical Reviewer.
    
    Your instructions:
    1. Identify logical flaws, mechanism gaps, or edge cases in their proposal.
    2. Propose a counter-hypothesis or challenge their assumptions using established neuroscience literature.
    3. Do NOT just give them the answer. Instead, ask piercing questions that force them to rethink their computational model or biological mechanism.
    4. Keep your critique concise, sharp, and scientifically rigorous.
    
    The user will provide the student team's pitch text. Respond with your critique.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Team's Pitch summary:\n\n{pitch_text}")
    ])
    
    return prompt

def run_coscientist_review(llm, pitch_text: str) -> str:
    """
    Generates a rigorous peer-review simulation for the student pitch.
    llm should be a conversational model.
    """
    prompt = get_coscientist_prompt()
    chain = prompt | llm | StrOutputParser()
    
    response = chain.invoke({"pitch_text": pitch_text})
    return response

if __name__ == "__main__":
    print("AI-CoScientist Simulator Agent initialized.")
