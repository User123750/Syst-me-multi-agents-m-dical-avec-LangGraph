from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Serveur_Medical_Base_De_Donnees")

@mcp.tool()
def get_patient_history(patient_id: str) -> str:
    """
    Récupère l'historique médical d'un patient à partir de son identifiant (ex: P123).
    """
    print(f"🔍 [MCP Server] Requête reçue pour le patient : {patient_id}")
    
    base_de_donnees = {
        "P123": "Antécédents : Diabète de type 2. Allergies : Pénicilline.",
        "P456": "Antécédents : Hypertension. Opération du genou en 2021.",
        "P789": "Antécédents : Insuffisance veineuse. Allergies : Aucune."
    }
    
    return base_de_donnees.get(patient_id, " Aucun dossier trouvé pour ce patient.")


if __name__ == "__main__":
    print(" Serveur MCP Python démarré...")
    mcp.run()