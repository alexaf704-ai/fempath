import streamlit as st
from groq import Groq
import json
import time

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="FemPath — AI Career Co-Pilot",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── CUSTOM CSS (Restaurado) ──────────────────────────────────
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

.quiz-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,192,127,0.2);
    border-radius: 20px;
    padding: 36px;
    margin-bottom: 24px;
    position: relative;
}
.quiz-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #00C07F, #7c3aed);
    border-radius: 20px 20px 0 0;
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

.stButton > button {
    background: #00C07F !important;
    color: #0d1b2a !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
    width: 100% !important;
}

/* Clases de Resultados */
.result-hero { text-align: center; padding: 32px 0; }
.track-pill { display: inline-block; background: rgba(0,192,127,0.12); border: 2px solid #00C07F; color: #00C07F; padding: 5px 16px; border-radius: 20px; text-transform: uppercase; font-size: 12px; font-weight: 800; }
.week-box { background: rgba(0,192,127,0.08); border: 1px solid #00C07F; border-radius: 18px; padding: 26px; margin-bottom: 24px; }
.action-item { background: rgba(255,255,255,0.04); border-radius: 12px; padding: 16px; margin-bottom: 10px; display: flex; gap: 12px; }
.action-num { background: #00C07F; color: #0d1b2a; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; }
.phase-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 20px; margin-bottom: 12px; }
.res-card { background: rgba(255,255,255,0.03); border-radius: 14px; padding: 18px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# ── PROMPTS ──────────────────────────────────────────────────
SYSTEM_PROMPT = """Eres el AI de FemPath — un co-piloto de carrera para mujeres en el ecosistema tech y venture capital de México.
Responde ÚNICAMENTE con JSON válido."""

def build_prompt(name, interest, goal, strength, timeline):
    return f"""Genera un roadmap personalizado para {name}. Interés: {interest}, Meta: {goal}, Fortaleza: {strength}, Tiempo: {timeline}.
    Responde con este JSON exacto: {{
      "track_name": "string", "track_icon": "emoji", "title": "string", "description": "string", "insight": "string",
      "week_actions": [{{ "title": "string", "detail": "string", "cta": "string" }}],
      "roadmap": [{{ "phase": "string", "title": "string", "actions": ["string"] }}],
      "resources": [{{ "title": "string", "why": "string", "desc": "string" }}]
    }}"""

# ── LOGICA GROQ ─────────────────────────────────────────────
def call_groq(name, interest, goal, strength, timeline):
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("⚠️ Falta la GROQ_API_KEY en los Secrets.")
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

# ── RENDER RESULT (Restaurado) ──────────────────────────────
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
        with st.container():
            st.markdown(f"""<div class="phase-card"><strong>{p['phase']}: {p['title']}</strong><br>
            <small>• {'<br>• '.join(p['actions'])}</small></div>""", unsafe_allow_html=True)

    if st.button("↩ Crear otra ruta"):
        st.session_state.result = None
        st.rerun()

# ── MAIN ─────────────────────────────────────────────────────
def main():
    if "result" not in st.session_state: st.session_state.result = None

    st.markdown('<div class="hero-tag">🚀 MAD Fellows Challenge 2026 · Track 02</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">El <span class="hl">co-piloto de AI</span> para tu carrera</div>', unsafe_allow_html=True)

    if st.session_state.result:
        render_result(st.session_state.result)
        return

    # Stats Row (Restaurado)
    st.markdown("""
    <div class="stat-row">
      <div class="stat-box"><div class="stat-num">15%</div><div class="stat-lbl">Capital VC a startups de mujeres</div></div>
      <div class="stat-box"><div class="stat-num">52¢</div><div class="stat-lbl">Por cada peso que recibe un hombre</div></div>
      <div class="stat-box"><div class="stat-num">10%</div><div class="stat-lbl">Deal flow femenino en México</div></div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("quiz"):
        name = st.text_input("¿Cómo te llamas?")
        interest = st.selectbox("Interés", ["Venture Capital", "Tecnología", "Impacto Social"])
        goal = st.selectbox("Meta", ["Fundadora", "Inversionista", "Líder Corporativa"])
        strength = st.selectbox("Fortaleza", ["Análisis de Datos", "Networking", "Creatividad"])
        timeline = st.selectbox("Horizonte", ["Ahora mismo", "Al graduarme"])
        
        if st.form_submit_button("✨ Generar Roadmap"):
            if name:
                with st.spinner("Llama 3 analizando..."):
                    try:
                        st.session_state.result = call_groq(name, interest, goal, strength, timeline)
                        st.rerun()
                    except Exception as e: st.error(f"Error: {e}")
            else: st.warning("Escribe tu nombre.")

if __name__ == "__main__": main()
