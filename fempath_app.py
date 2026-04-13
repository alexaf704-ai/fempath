import streamlit as st
from groq import Groq
import json
import time

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="FemPath — AI Career Co-Pilot",
    page_icon="🚀",
    layout="centered"
)

# ── CUSTOM CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0d1b2a; color: #ffffff; }
.stApp { background-color: #0d1b2a; }
#MainMenu, footer, header { visibility: hidden; }
.hero-tag { display: inline-block; background: rgba(0,192,127,0.1); border: 1px solid rgba(0,192,127,0.3); color: #00C07F; padding: 5px 14px; border-radius: 20px; font-size: 12px; font-weight: 700; margin-bottom: 16px; }
.hero-title { font-size: 40px; font-weight: 900; line-height: 1.1; margin-bottom: 14px; }
.hero-title .hl { color: #00C07F; }
.stButton > button { background: #00C07F !important; color: #0d1b2a !important; font-weight: 800 !important; width: 100% !important; border-radius: 12px !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

# ── LÓGICA DE GROQ AI ───────────────────────────────────────
def call_groq(name, interest, goal, strength, timeline):
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("⚠️ Falta la GROQ_API_KEY en los Secrets de Streamlit.")
        st.stop()

    client = Groq(api_key=api_key)
    
    system_msg = """Eres la IA de FemPath. Tu misión es empoderar a mujeres en el ecosistema emprendedor del ITAM.
    Genera un roadmap con: track_name, track_icon, insight (un consejo potente), 
    week_actions (3 acciones con title, detail, cta) y resources.
    Responde ÚNICAMENTE en formato JSON."""

    prompt = f"Perfil: {name}, Interés: {interest}, Meta: {goal}, Fortaleza: {strength}, Tiempo: {timeline}."

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

# ── INTERFAZ DE USUARIO ──────────────────────────────────────
def main():
    if "result" not in st.session_state: st.session_state.result = None

    st.markdown('<div class="hero-tag">🚀 MAD Fellows Challenge 2026 · Track #2</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">FemPath: Tu <span class="hl">co-piloto</span> hacia el EPIC Lab</div>', unsafe_allow_html=True)

    if st.session_state.result:
        res = st.session_state.result
        st.success(f"¡Listo, {res.get('track_name', 'Emprendedora')}!")
        st.info(f"💡 **Insight:** {res.get('insight')}")
        
        for act in res.get('week_actions', []):
            with st.expander(f"📌 {act['title']}"):
                st.write(act['detail'])
                st.caption(f"Acción: {act['cta']}")
        
        if st.button("Crear otro Roadmap"):
            st.session_state.result = None
            st.rerun()
        return

    with st.form("quiz"):
        name = st.text_input("¿Cómo te llamas?")
        interest = st.selectbox("¿Qué te interesa?", ["Venture Capital", "Fintech", "EdTech", "Sostenibilidad"])
        goal = st.selectbox("¿Tu meta?", ["Fundar una startup", "Ser Inversionista", "Liderar en Tech"])
        strength = st.selectbox("Tu mayor fortaleza", ["Análisis de Datos", "Networking", "Estrategia"])
        timeline = st.selectbox("¿Cuándo quieres empezar?", ["Ahora mismo", "Próximo semestre"])

        if st.form_submit_button("Generar Plan con Groq AI"):
            if name:
                with st.spinner("Llama 3 analizando tu perfil..."):
                    try:
                        st.session_state.result = call_groq(name, interest, goal, strength, timeline)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Escribe tu nombre para continuar.")

    st.markdown("<br><hr><center><small>Powered by Groq (Llama 3.3) · Hecho para EPIC Lab ITAM</small></center>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
