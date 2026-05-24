from langchain_core.tools import tool

@tool
def ask_patient(question: str) -> str:
    """
    Outil obligatoire pour poser une question au patient.
    À utiliser pour recueillir des informations cliniques successives.
    """
    return f"Question envoyée au patient : {question}"