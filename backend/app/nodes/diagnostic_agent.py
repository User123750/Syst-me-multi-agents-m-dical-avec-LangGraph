import os
import asyncio
import nest_asyncio
from langchain_ollama import ChatOllama 
from app.state import MedicalState
from langchain_core.messages import AIMessage, SystemMessage
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

nest_asyncio.apply()

llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0.2)

async def get_mcp_data(patient_id: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_server = os.path.abspath(os.path.join(current_dir, "../../../mcp_server/server.py"))
    
    server_params = StdioServerParameters(
        command="python",
        args=[path_to_server]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("get_patient_history", arguments={"patient_id": patient_id})
                return result.content[0].text
    except Exception:
        return "Aucun antécédent trouvé."

def diagnostic_node(state: MedicalState):
    messages = state.get("messages", [])
    question_count = state.get("question_count", 0)
    
    patient_id = "P123" 
    
    if question_count < 5:
        antecedents = asyncio.run(get_mcp_data(patient_id))
        
        prompt = (
            "Tu es un médecin virtuel menant un interrogatoire clinique strict.\n"
            f"DOSSIER DU PATIENT (Lu via MCP) : {antecedents}\n"
            "Règles :\n"
            "1. Prends OBLIGATOIREMENT en compte ces antécédents dans tes questions si c'est pertinent (ex: allergies, maladies chroniques).\n"
            "2. Lis attentivement la TOUTE DERNIÈRE réponse du patient.\n"
            "3. Ne repose JAMAIS une question dont tu as déjà la réponse.\n"
            "4. Pose STRICTEMENT UNE SEULE NOUVELLE QUESTION logique pour faire avancer le diagnostic.\n"
            "5. Ne fais aucun diagnostic."
        )
        
        reponse_ia = llm.invoke([SystemMessage(content=prompt)] + messages)
        
        return {
            "question_count": question_count + 1,
            "messages": [AIMessage(content=reponse_ia.content)]
        }
        
    else:
        antecedents = asyncio.run(get_mcp_data(patient_id))
        
        prompt_summary = (
            "Tu es maintenant un assistant de synthèse médicale. TU NE PARLES PLUS AU PATIENT. "
            f"Antécédents du patient : {antecedents}\n"
            "Ta seule tâche est de rédiger une synthèse clinique sous forme de puces (Antécédents, Motif, Localisation, Symptômes) pour le médecin traitant. "
            "NE POSE AUCUNE QUESTION. Ne fais aucun diagnostic."
        )
        res_summary = llm.invoke([SystemMessage(content=prompt_summary)] + messages)
        
        prompt_care = "Génère des recommandations de premier secours basées sur ces symptômes."
        res_care = llm.invoke([SystemMessage(content=prompt_care)] + messages)
        
        return {
            "diagnostic_summary": res_summary.content,
            "interim_care": res_care.content
        }