from langgraph.graph import StateGraph, START, END
from app.state import MedicalState
from app.nodes.diagnostic_agent import diagnostic_node
from app.nodes.physician_review import physician_node
from app.nodes.report_agent import report_node
from app.nodes.supervisor import supervisor_node

workflow = StateGraph(MedicalState)

workflow.add_node("diagnostic_agent", diagnostic_node)
workflow.add_node("physician_review", physician_node)
workflow.add_node("report_agent", report_node)

workflow.add_conditional_edges(
    START, 
    supervisor_node, 
    {
        "diagnostic_agent": "diagnostic_agent",
        "physician_review": "physician_review",
        "report_agent": "report_agent",
        "END": END
    }
)

workflow.add_edge("diagnostic_agent", END)
workflow.add_edge("physician_review", END)
workflow.add_edge("report_agent", END)

# L'API devient propre et pure (sans mémoire interne cachée)
app_graph = workflow.compile()