import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generate_the_hook(llm, topic: str, related_literature_summary: str) -> str:
    """
    Generates 'The Hook' for the first 10 minutes of the class.
    This replaces a didactic lecture with an impassable brain science puzzle or a mission.
    """
    system_prompt = """
    You are an avant-garde professor teaching Brain-Mind-Behavior neuro-data science.
    You are creating "The Hook" for a new week's topic. You have exactly 10 minutes to present this.
    Instead of lecturing theoretically, present a seemingly contradictory clinical case, a massive dataset anomaly, or a philosophical/computational impossibility relevant to the topic.
    
    Structure:
    1. The Setup (A striking phenomenon)
    2. The Contradiction (Why current textbook theories fail here)
    3. The Challenge (The mission the 5-team groups must solve with NotebookLM/Agentic AI in the next 30 minutes)
    
    Format output as Markdown slides (using ---).
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Topic: {topic}\nLiterature Context:\n{context}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"topic": topic, "context": related_literature_summary})

if __name__ == "__main__":
    print("Material Generator Agent loaded.")
