from app.state import MedicalState

def supervisor_node(state: MedicalState):
    if state.get("final_report"):
        return "END"
    if state.get("physician_treatment"):
        return "report_agent"
    if state.get("diagnostic_summary"):
        return "physician_review"
    return "diagnostic_agent"