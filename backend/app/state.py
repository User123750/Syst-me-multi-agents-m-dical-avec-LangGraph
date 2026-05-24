from typing import TypedDict, List, Annotated
from langchain_core.messages import AnyMessage
import operator

class MedicalState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]
    question_count: int
    diagnostic_summary: str
    interim_care: str
    physician_treatment: str
    final_report: str