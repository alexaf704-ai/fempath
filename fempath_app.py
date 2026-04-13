import streamlit as st
from groq import Groq
import json
import time

# ── CONFIGURACIÓN DE PÁGINA ──────────────────────────────────
st.set_page_config(
    page_title="FemPath — AI Career Co-Pilot",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── DISEÑO CSS PERSONALIZADO (Cierre verificado) ─────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d1b2a;
    color: #ffffff;
}
.stApp { background-color: #0d1b2a; }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2rem 4rem; max-width: 780px; }

.hero-tag {
    display: inline-block;
    background: rgba(0,192,127,0.1);
    border: 1px solid rgba(0,192,127,0.3);
    color: #00C07F;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 16px;
}
.hero-title {
    font-size: clamp(32px, 5vw, 56px);
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 14px;
}
.hero-title .hl { color: #00C07F; }
.hero-sub {
    font-size: 16px;
    color: #8fa3b8;
    line-height: 1.65;
    margin-bottom: 32px;
    max-width: 600px;
}

.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 36px;
}
.stat-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px 14px;
    text-align: center;
}
.stat-num { font-size: 32px; font-weight: 900; color: #00C07F; }
.stat-lbl { font-size: 11px; color: #8fa3b8; margin-top: 6px; }

.stButton > button {
    background: #00C07F !important;
    color: #0d1b2a !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
    width: 100% !important;
    border: none !important;
    padding: 10px !important;
}

.ai-bubble {
    background: rgba(0,192,127,0.07);
    border: 1px solid rgba(0,192,127,0.18);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 13px;
    color: rgba(255,255,255,0.75);
    margin-bottom: 24px;
}

/* Resultados */
.result-hero { text-align: center; padding: 32px 0; }
.track-pill { display: inline-block; background: rgba(0,192,127,0.12); border: 2px solid #00C07F; color: #00C07F; padding: 5px 16px; border-radius: 20px; text-transform: uppercase; font-size: 12px; font-weight: 800; }
.week-box { background: rgba(0,192,127,0.08); border: 1px solid #00C07F; border-radius: 18px; padding: 26px; margin-bottom: 24px; }
.action-item { background: rgba(255,255,255,0.04); border-radius: 12px; padding: 16px; margin-bottom: 10px; display: flex; gap: 12px; }
.action-num { background: #00C07F; color: #0d1b2a; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; }
.phase-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 20px; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# ── LÓGICA DE IA (GROQ) ──────────────────────────────────────
SYSTEM_PROMPT = """Eres la IA de FemPath. Tu misión es empoderar a mujeres en el ecosistema del ITAM. 
Responde ÚNICAMENTE con JSON válido."""

def build_prompt(name, interest, goal, strength, timeline):
    return f"""Genera un roadmap para {name}. Interés: {interest}, Meta: {goal}, Fortaleza: {strength}, Tiempo: {timeline}.
    Formato JSON: {{
      "track_name": "string", "track_icon": "emoji", "title": "string", "description": "string", "insight": "string",
      "week_actions": [{{ "title": "string", "detail": "string", "cta": "string" }}],
      "roadmap": [{{ "phase": "string", "title": "string", "actions": ["string"] }}]
    }}"""

def call_groq(name, interest, goal, strength, timeline):
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("⚠️ Agrega la GROQ_API_KEY en los Secrets de Streamlit.")
        st.stop()

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(name, interest, goal, strength, timeline)}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# ── RENDERIZADO DE RESULTADOS ────────────────────────────────
def render_result(data):
    st.markdown(f"""
    <div class="result-hero">
      <span style="font-size: 56px;">{data['track_icon']}</span><br>
      <div class="track-pill">{data['track_name']}</div>
      <div class="hero-title">{data['title']}</div>
      <div class="hero-sub">{data['description']}</div>
    </div>
    <div class="ai-bubble">🤖 <strong>Insight:</strong> {data['insight']}</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="week-box"><strong>🔥 Acciones para esta semana:</strong>', unsafe_allow_html=True)
    for i, a in enumerate(data['week_actions'], 1):
        st.markdown(f"""
        <div class="action-item">
          <div class="action-num">{i}</div>
          <div><strong>{a['title']}</strong><br><small>{a['detail']}</small></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🗺️ Tu Roadmap")
    for p in data['roadmap']:
        st.markdown(f"""<div class="phase-card"><strong>{p['phase']}: {p['title']}</strong><br>
        <small>• {'<br>• '.join(p['actions'])}</small></div>""", unsafe_allow_html=True)

    if st.button("↩ Crear otra ruta"):
        st.session_state.result = None
        st.rerun()

# ── APLICACIÓN PRINCIPAL ─────────────────────────────────────
def main():
    if "result" not in st.session_state: st.session_state.result = None

    st.markdown('<div class="hero-tag">🚀 MAD Fellows Challenge 2026 · Track 02</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">FemPath: Tu <span class="hl">co-piloto</span> de carrera</div>', unsafe_allow_html=True)

    if st.session_state.result:
        render_result(st.session_state.result)
        return

    # Sección de Estadísticas (Ajustadas para México)
    st.markdown("""
    <div class="stat-row">
      <div class="stat-box">
        <div class="stat-num">15%</div>
        <div class="stat-lbl">Capital VC a startups de mujeres</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">52<span style="font-size:18px">¢</span></div>
        <div class="stat-lbl">Centavos por cada peso que gana un hombre</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">10%</div>
        <div class="stat-lbl">Deal flow femenino en México</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("quiz"):
        name = st.text_input("¿Cómo te llamas?")
        interest = st.selectbox("¿Qué sector te apasiona?", ["Venture Capital", "Tecnología / Startups", "Impacto Social"])
        goal = st.selectbox("Tu meta a futuro", ["Fundar una empresa", "Ser Inversionista", "Liderazgo en Tech"])
        strength = st.selectbox("Tu mayor fortaleza", ["Análisis de Datos", "Networking", "Creatividad y Diseño"])
        timeline = st.selectbox("¿Cuándo quieres empezar?", ["Ahora mismo", "Al graduarme"])
        
        if st.form_submit_button("✨ Generar Mi Ruta con IA"):
            if name:
                with st.spinner("Llama 3 analizando tu perfil..."):
                    try:
                        st.session_state.result = call_groq(name, interest, goal, strength, timeline)
                        st.rerun()
                    except Exception as e: 
                        st.error(f"Hubo un detalle: {e}")
            else: 
                st.warning("Por favor escribe tu nombre.")

if __name__ == "__main__":
    main()
