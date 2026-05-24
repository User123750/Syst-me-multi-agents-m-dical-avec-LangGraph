from langchain_ollama import ChatOllama 
from app.state import MedicalState
from langchain_core.messages import AIMessage, SystemMessage

llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0)

def report_node(state: MedicalState):
    print("📝 ReportAgent : Je rédige le rapport final...")
    summary = state.get("diagnostic_summary", "Aucune synthèse.")
    treatment = state.get("physician_treatment", "Aucun traitement.")
    
    prompt = (
        "Tu es un médecin chef. Rédige un compte rendu final structuré.\n"
        f"Synthèse : {summary}\nTraitement : {treatment}\n\n"
        "Format : ### Motif et Synthèse \n[Texte]\n ### Décision et Traitement \n[Texte]"
    )
    
    reponse_ia = llm.invoke([SystemMessage(content=prompt)])
    
    return {
        "final_report": reponse_ia.content,
        "messages": [AIMessage(content="Rapport final généré.")]
    }