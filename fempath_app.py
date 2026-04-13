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

# ── CUSTOM CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d1b2a;
    color: #ffffff;
}
.stApp { background-color: #0d1b2a; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2rem 4rem; max-width: 780px; }

/* Hero */
.hero-tag {
    display: inline-block;
    background: rgba(0,192,127,0.1);
    border: 1px solid rgba(0,192,127,0.3);
    color: #00C07F;
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .5px;
    margin-bottom: 16px;
}
.hero-title {
    font-size: clamp(32px, 5vw, 56px);
    font-weight: 900;
    line-height: 1.1;
    letter-spacing: -1.5px;
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

/* Stat row */
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
.stat-num { font-size: 32px; font-weight: 900; color: #00C07F; line-height: 1; }
.stat-lbl { font-size: 11px; color: #8fa3b8; margin-top: 6px; line-height: 1.4; }

/* Quiz card */
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
.quiz-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #00C07F;
    margin-bottom: 20px;
}
.ai-bubble {
    background: rgba(0,192,127,0.07);
    border: 1px solid rgba(0,192,127,0.18);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 13px;
    color: rgba(255,255,255,0.75);
    line-height: 1.5;
    margin-bottom: 24px;
}

/* Streamlit selectbox override */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 2px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: white !important;
}
.stSelectbox > div > div:hover {
    border-color: #00C07F !important;
}

/* Button */
.stButton > button {
    background: #00C07F !important;
    color: #0d1b2a !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    padding: 14px 36px !important;
    border-radius: 12px !important;
    border: none !important;
    width: 100% !important;
    transition: all .2s !important;
    font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    background: #009962 !important;
    transform: translateY(-1px);
    box-shadow: 0 6px 24px rgba(0,192,127,0.3) !important;
}

/* Result sections */
.result-hero {
    text-align: center;
    padding: 32px 0 24px;
    border-bottom: 1px solid rgba(255,255,255,0.07);
    margin-bottom: 28px;
}
.result-icon { font-size: 56px; display: block; margin-bottom: 12px; }
.track-pill {
    display: inline-block;
    background: rgba(0,192,127,0.12);
    border: 2px solid #00C07F;
    color: #00C07F;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 5px 16px;
    border-radius: 20px;
    margin-bottom: 14px;
}
.result-title { font-size: 26px; font-weight: 800; margin-bottom: 10px; }
.result-desc { font-size: 14px; color: #8fa3b8; line-height: 1.65; max-width: 520px; margin: 0 auto; }

/* This week */
.week-box {
    background: linear-gradient(135deg, rgba(0,192,127,0.08), rgba(124,58,237,0.06));
    border: 1px solid rgba(0,192,127,0.28);
    border-radius: 18px;
    padding: 26px;
    margin-bottom: 24px;
}
.week-title {
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.action-item {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
    display: grid;
    grid-template-columns: 32px 1fr auto;
    gap: 12px;
    align-items: start;
}
.action-num {
    width: 28px; height: 28px;
    background: #00C07F;
    color: #0d1b2a;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 800;
    flex-shrink: 0;
}
.action-title { font-size: 13px; font-weight: 700; margin-bottom: 4px; }
.action-sub { font-size: 12px; color: #8fa3b8; line-height: 1.4; }
.action-cta {
    font-size: 11px; font-weight: 700;
    color: #00C07F;
    background: rgba(0,192,127,0.1);
    padding: 4px 10px;
    border-radius: 20px;
    white-space: nowrap;
}

/* Roadmap */
.phase-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 12px;
}
.phase-label {
    font-size: 11px; font-weight: 700;
    letter-spacing: 1.5px; text-transform: uppercase;
    color: #00C07F; margin-bottom: 8px;
}
.phase-title { font-size: 15px; font-weight: 700; margin-bottom: 10px; }
.phase-actions { list-style: none; padding: 0; }
.phase-actions li {
    font-size: 13px; color: #8fa3b8;
    padding: 4px 0 4px 18px;
    position: relative; line-height: 1.4;
}
.phase-actions li::before {
    content: '→';
    position: absolute; left: 0;
    color: #00C07F; font-weight: 700;
}

/* Resource cards */
.res-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 10px;
}
.res-title { font-size: 14px; font-weight: 700; margin-bottom: 4px; }
.res-why { font-size: 12px; color: #00C07F; font-style: italic; margin-bottom: 6px; }
.res-desc { font-size: 12px; color: #8fa3b8; }

/* Section header */
.sec-hdr {
    font-size: 11px; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    color: #00C07F; margin: 28px 0 12px;
}

/* AI tools badge */
.tools-row {
    display: flex; gap: 8px; flex-wrap: wrap;
    margin-top: 28px; padding-top: 20px;
    border-top: 1px solid rgba(255,255,255,0.06);
}
.tool-chip {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 11px; color: #8fa3b8;
}
</style>
""", unsafe_allow_html=True)


# ── GROQ PROMPT ──────────────────────────────────────────────
SYSTEM_PROMPT = """Eres el AI de FemPath — un co-piloto de carrera para mujeres en el ecosistema tech y venture capital de México.

Tu rol es analizar el perfil de la usuaria y generar una respuesta ALTAMENTE PERSONALIZADA y CONCRETA.

REGLAS CRÍTICAS:
- Sé específica: nombra fondos reales (ALLVP, Dux Capital, 500 Startups MX), empresas reales, programas reales en México
- Las acciones deben ser ejecutables ESTA SEMANA, no genéricas
- El tono es de mentora experta: directa, cálida, sin condescendencia
- Responde ÚNICAMENTE con JSON válido, sin texto adicional"""

def build_prompt(name, interest, goal, strength, timeline):
    return f"""Analiza este perfil y genera un roadmap personalizado:

PERFIL:
- Nombre: {name}
- Interés principal: {interest}
- Meta en 5 años: {goal}
- Mayor fortaleza: {strength}
- Horizonte de tiempo: {timeline}

Responde con este JSON exacto (sin markdown, sin texto extra):

{{
  "track_name": "nombre del track",
  "track_icon": "emoji",
  "title": "Tu camino: [título]",
  "description": "2-3 oraciones personalizadas",
  "insight": "1 oración de insight real",
  "week_actions": [
    {{
      "title": "acción específica #1",
      "detail": "instrucciones específicas con recursos de México",
      "cta": "etiqueta corta"
    }},
    {{
      "title": "acción #2",
      "detail": "instrucciones específicas",
      "cta": "etiqueta corta"
    }},
    {{
      "title": "acción #3",
      "detail": "instrucciones específicas",
      "cta": "etiqueta corta"
    }}
  ],
  "roadmap": [
    {{
      "phase": "0 – 3 meses",
      "title": "título",
      "actions": ["acción 1", "acción 2", "acción 3", "acción 4"]
    }},
    {{
      "phase": "3 – 12 meses",
      "title": "título",
      "actions": ["acción 1", "acción 2", "acción 3", "acción 4"]
    }},
    {{
      "phase": "1 – 3 años",
      "title": "título",
      "actions": ["acción 1", "acción 2", "acción 3", "acción 4"]
    }}
  ],
  "resources": [
    {{ "title": "recurso 1", "why": "razón", "desc": "descripción" }},
    {{ "title": "recurso 2", "why": "razón", "desc": "descripción" }},
    {{ "title": "recurso 3", "why": "razón", "desc": "descripción" }},
    {{ "title": "recurso 4", "why": "razón", "desc": "descripción" }}
  ]
}}"""


# ── HELPERS ──────────────────────────────────────────────────
def call_groq(name, interest, goal, strength, timeline):
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("⚠️ Agrega tu GROQ_API_KEY en los secrets de Streamlit.")
        st.stop()

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_prompt(name, interest, goal, strength, timeline)}
        ],
        temperature=0.7,
        max_tokens=2000,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


def render_result(data):
    # Hero
    st.markdown(f"""
    <div class="result-hero">
      <span class="result-icon">{data['track_icon']}</span>
      <div class="track-pill">{data['track_name']}</div>
      <div class="result-title">{data['title']}</div>
      <div class="result-desc">{data['description']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Insight
    st.markdown(f"""
    <div class="ai-bubble">
      🤖 <strong>Insight de tu perfil:</strong> {data['insight']}
    </div>
    """, unsafe_allow_html=True)

    # This week actions
    actions_html = ""
    for i, a in enumerate(data['week_actions'], 1):
        actions_html += f"""
        <div class="action-item">
          <div class="action-num">{i}</div>
          <div>
            <div class="action-title">{a['title']}</div>
            <div class="action-sub">{a['detail']}</div>
          </div>
          <span class="action-cta">{a['cta']}</span>
        </div>"""

    st.markdown(f"""
    <div class="week-box">
      <div class="week-title">🔥 Tus 3 acciones concretas <u>esta semana</u>
        <span style="font-size:12px;color:#8fa3b8;font-weight:400"> — generadas por Groq AI</span>
      </div>
      {actions_html}
    </div>
    """, unsafe_allow_html=True)

    # Roadmap
    st.markdown('<div class="sec-hdr">🗺️ Tu Roadmap de Carrera (3 fases)</div>', unsafe_allow_html=True)
    for phase in data['roadmap']:
        items = "".join(f"<li>{a}</li>" for a in phase['actions'])
        st.markdown(f"""
        <div class="phase-card">
          <div class="phase-label">{phase['phase']}</div>
          <div class="phase-title">{phase['title']}</div>
          <ul class="phase-actions">{items}</ul>
        </div>
        """, unsafe_allow_html=True)

    # Resources
    st.markdown('<div class="sec-hdr">🤖 Recursos recomendados por Groq AI</div>', unsafe_allow_html=True)
    for r in data['resources']:
        st.markdown(f"""
        <div class="res-card">
          <div class="res-title">{r['title']}</div>
          <div class="res-why">"{r['why']}"</div>
          <div class="res-desc">{r['desc']}</div>
        </div>
        """, unsafe_allow_html=True)

    # AI Tools used
    st.markdown("""
    <div class="tools-row">
      <span style="font-size:11px;color:#8fa3b8;align-self:center">🤖 Powered by:</span>
      <span class="tool-chip">Llama 3.3 (Groq)</span>
      <span class="tool-chip">ChatGPT (UX design)</span>
      <span class="tool-chip">Claude (arquitectura)</span>
      <span class="tool-chip">Gamma (pitch deck)</span>
      <span class="tool-chip">Streamlit (deploy)</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    if st.button("↩ Explorar otro camino"):
        st.session_state.result = None
        st.rerun()


# ── MAIN APP ─────────────────────────────────────────────────
def main():
    if "result" not in st.session_state:
        st.session_state.result = None

    # Header
    st.markdown("""
    <div class="hero-tag">🚀 MAD Fellows Challenge 2026 · EPIC Lab · ITAM · Track 02</div>
    <div class="hero-title">El <span class="hl">co-piloto de AI</span><br/>para tu carrera<br/>en Tech & VC</div>
    <div class="hero-sub">
      FemPath te ayuda a llegar con rutas personalizadas generadas por Groq AI para el ecosistema de México.
    </div>
    """, unsafe_allow_html=True)

    # Stats Row
    st.markdown("""
    <div class="stat-row">
      <div class="stat-box">
        <div class="stat-num">15%</div>
        <div class="stat-lbl">Del capital VC en LATAM va a startups de mujeres</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">52<span style="font-size:18px">¢</span></div>
        <div class="stat-lbl">Centavos por cada peso que gana un hombre en inversión</div>
      </div>
      <div class="stat-box">
        <div class="stat-num">10%</div>
        <div class="stat-lbl">Del deal flow en fondos VC de México proviene de mujeres</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.result:
        render_result(st.session_state.result)
        return

    # Quiz card
    st.markdown("""
    <div class="quiz-card">
      <div class="quiz-label">🤖 AI Pathfinder — Tu ruta personalizada</div>
      <div class="ai-bubble">
        Hola, soy el AI de FemPath. Generaré tu roadmap de carrera con acciones concretas para esta semana.
      </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("quiz_form"):
        name = st.text_input("¿Cómo te llamas?", placeholder="Ej: Ana, Mariana…")
        interest = st.selectbox("¿Área de interés?", ["Selecciona...", "Finanzas y VC", "Tecnología", "Impacto Social", "Estrategia"])
        goal = st.selectbox("¿Tu meta en 5 años?", ["Selecciona...", "Fundadora", "Inversionista", "Líder en Corporativo", "Construir ecosistema"])
        strength = st.selectbox("¿Mayor fortaleza?", ["Selecciona...", "Análisis Cuantitativo", "Networking", "Creatividad", "Ejecución"])
        timeline = st.selectbox("¿Horizonte?", ["Selecciona...", "Ahora mismo", "Este año", "Al graduarme", "Experiencia previa"])
        
        submitted = st.form_submit_button("✨ Generar mi roadmap con Groq AI")

    if submitted:
        invalid = any(v.startswith("Selecciona") for v in [interest, goal, strength, timeline])
        if not name.strip():
            st.error("👋 Escribe tu nombre.")
        elif invalid:
            st.error("⚠️ Responde todas las preguntas.")
        else:
            with st.spinner("🤖 Generando tu roadmap personalizado..."):
                try:
                    result = call_groq(name.strip(), interest, goal, strength, timeline)
                    st.session_state.result = result
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    # Footer
    st.markdown("""
    <div style="text-align:center;margin-top:48px;padding-top:20px;
    border-top:1px solid rgba(255,255,255,0.06);font-size:12px;color:#8fa3b8;">
      FemPath · AI Career Co-Pilot · MAD Fellows Challenge 2026 · EPIC Lab ITAM<br/>
      <span style="color:#00C07F">Powered by Groq AI (Llama 3.3)</span>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
