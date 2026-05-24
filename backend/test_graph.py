import os
from langchain_core.messages import HumanMessage


os.environ["GROQ_API_KEY"] = ""

from app.graph import app_graph
def run_test():
    print(" Démarrage de la simulation du workflow...")
    
    config = {"configurable": {"thread_id": "consultation_001"}, "recursion_limit": 25}
    
    initial_state = {
        "messages": [HumanMessage(content="Bonjour, j'ai des maux de tête terribles et de la fièvre depuis hier.")],
        "question_count": 0
    }

    try:
        for event in app_graph.stream(initial_state, config):
            for node_name, state_update in event.items():
                print(f" Nœud exécuté : {node_name}")
        
        current_state = app_graph.get_state(config)
        
        if current_state.next and current_state.next[0] == "physician_review":
            print("\n" + "="*50)
            print(" WORKFLOW EN PAUSE : INTERVENTION DU MÉDECIN REQUISE")
            print("="*50)
            
            print(f" Synthèse clinique : {current_state.values.get('diagnostic_summary')}")
            print(f" Recommandation provisoire : {current_state.values.get('interim_care')}")
            
            avis_medecin = input("\n Entrez votre décision/traitement : ")
            
            app_graph.update_state(
                config,
                {"physician_treatment": avis_medecin},
                as_node="physician_review" )
            
            print("\n REPRISE DU WORKFLOW...")
           
            for event in app_graph.stream(None, config):
                 for node_name, state_update in event.items():
                    print(f" Nœud exécuté : {node_name}")
                    
    except Exception as e:
        print(f"\nLe workflow s'est arrêté : {e}")

if __name__ == "__main__":
    run_test()