from langchain_core.tools import tool

@tool
def recommend_interim_care(symptoms: str) -> str:
    """
    Génère une recommandation intermédiaire prudente.
    Ne remplace JAMAIS l'avis d'un médecin.
    """
    return "Recommandation : Repos, hydratation, et surveillance. Consultez rapidement en cas d'aggravation."