from app.state import MedicalState
from langchain_core.messages import AIMessage

def physician_node(state: MedicalState):
    traitement_saisi = state.get("physician_treatment", "Aucun traitement spécifique saisi.")
    print("👨‍⚕️ PhysicianNode : Décision du médecin reçue.")
    
    return {
        "physician_treatment": traitement_saisi,
        "messages": [AIMessage(content="Le médecin a validé le dossier.")]
    }