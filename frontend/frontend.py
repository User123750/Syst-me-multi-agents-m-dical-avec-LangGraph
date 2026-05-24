import streamlit as st
import requests

st.set_page_config(page_title="Système IA Médical", layout="centered")
st.title(" Consultation Multi-Agents")
st.divider()

if "status" not in st.session_state:
    st.session_state.status = "Diagnostic" 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Bonjour, quels symptômes ressentez-vous ?"}]
if "summary" not in st.session_state:
    st.session_state.summary = None
if "care" not in st.session_state:
    st.session_state.care = None
if "report" not in st.session_state:
    st.session_state.report = None

for msg in st.session_state.chat_history:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg["content"])

if st.session_state.status == "Diagnostic":
    user_input = st.chat_input("Répondez ici...")
    
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.rerun()

    if st.session_state.chat_history[-1]["role"] == "user":
        with st.spinner("L'IA analyse vos réponses..."):
            res = requests.post(
                "http://127.0.0.1:8000/consultation/chat",
                json={"chat_history": st.session_state.chat_history}
            )
            if res.status_code == 200:
                data = res.json()
                if data.get("diagnostic_summary"):
                    st.session_state.status = "Attente_Medecin"
                    st.session_state.summary = data.get("diagnostic_summary")
                    st.session_state.care = data.get("interim_care")
                    st.rerun()
                else:
                    st.session_state.chat_history.append({"role": "assistant", "content": data["derniere_reponse"]})
                    st.rerun()
            else:
                st.error(f" Erreur détaillée : {res.text}")

elif st.session_state.status == "Attente_Medecin":
    st.info(" PAUSE : Validation médicale requise.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success(f" Synthèse :\n\n{st.session_state.summary}")
    with col2:
        st.warning(f" Recommandations :\n\n{st.session_state.care}")
    
    st.markdown("###  Espace Médecin")
    with st.form("doctor_form"):
        doctor_decision = st.text_area("Entrez la décision médicale :")
        submitted = st.form_submit_button("Générer le Rapport Final")
        
        if submitted and doctor_decision:
            with st.spinner("Génération..."):
                res = requests.post(
                    "http://127.0.0.1:8000/consultation/resume",
                    json={
                        "physician_treatment": doctor_decision, 
                        "chat_history": st.session_state.chat_history,
                        "diagnostic_summary": st.session_state.summary 
                    }
                )
                if res.status_code == 200:
                    st.session_state.status = "Termine"
                    st.session_state.report = res.json().get("final_report")
                    st.rerun()
                else:
                    st.error(f" Erreur  : {res.text}")

elif st.session_state.status == "Termine":
    st.success(" Consultation terminée.")
    st.markdown("###  Rapport Final")
    st.info(st.session_state.report)
    
    st.divider() 
    
    st.download_button(
        label=" Télécharger le rapport (.txt)",
        data=str(st.session_state.report),
        file_name="rapport_consultation.txt",
        mime="text/plain"
    )
    
    st.write("")
    
    if st.button(" Nouvelle consultation"):
        st.session_state.clear()
        st.rerun()