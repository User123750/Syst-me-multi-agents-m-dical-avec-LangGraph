from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.graph import app_graph
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

app = FastAPI(title="API Assistant Médical Agentique")

class ChatRequest(BaseModel):
    chat_history: list 
class ResumeRequest(BaseModel):
    physician_treatment: str
    chat_history: list

@app.post("/consultation/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        
        messages = []
        for msg in request.chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
                
      
        nb_questions = sum(1 for m in request.chat_history if m["role"] == "assistant") - 1
        
        inputs = {"messages": messages, "question_count": nb_questions}
        updated_state = app_graph.invoke(inputs, config={"configurable": {"thread_id": "1"}})
        
        derniers_msgs = updated_state.get("messages", [])
        reponse_ia = derniers_msgs[-1].content if derniers_msgs else ""
        
        return {
            "derniere_reponse": reponse_ia,
            "diagnostic_summary": updated_state.get("diagnostic_summary"),
            "interim_care": updated_state.get("interim_care")
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/consultation/resume")
async def resume_endpoint(request: ResumeRequest):
    try:
        messages = []
        for msg in request.chat_history:
            if msg["role"] == "user": 
                messages.append(HumanMessage(content=msg["content"]))
            else: 
                messages.append(AIMessage(content=msg["content"]))
                
        inputs = {"messages": messages, "physician_treatment": request.physician_treatment}
        updated_state = app_graph.invoke(inputs, config={"configurable": {"thread_id": "1"}})
        
        return {"final_report": updated_state.get("final_report")}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))