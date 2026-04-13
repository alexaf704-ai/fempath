import streamlit as st
from groq import Groq
import json
import time

# ── 1. CONFIGURACIÓN DE LA PÁGINA ──────────────────────────────
st.set_page_config(
    page_title="FemPath — AI Career Co-Pilot",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── 2. ESTILOS CSS (Sincronizados y con colores forzados) ──────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

/* Reset de colores para que nada sea invisible */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Inter', sans-serif;
    background-color: #0d1b2a !important;
    color: #ffffff !important;
}
.stApp { background-color: #0d1b2a; }

/* Forzar color blanco en todos los encabezados */
h1, h2, h3, h4, p, span, label {
    color: #ffffff !important;
}

#MainMenu, footer, header { visibility: hidden; }

/* Hero Section */
.hero-tag {
    display: inline-block;
    background: rgba(0,192,127,0.1);
    border: 1px solid rgba(0,192,127,0.3);
    color: #00C07F !important;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 20px;
}
.hero-title {
    font-size: clamp(32px, 5vw, 56px);
    font-weight: 900;
    line-height: 1.1;
    margin-bottom: 14px;
    color: #ffffff !important;
}
.hero-title .hl { color: #00C07F !important; }

/* Stats Row */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin: 40px 0;
}
.stat-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}
.stat-num { font-size: 32px; font-weight: 900; color: #00C07F !important; }
.stat-lbl { font-size: 11px; color: #8fa3b8 !important; margin-top: 6px; }

/* Problem Cards (Del HTML) */
.problem-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
    margin: 40px 0;
}
.pcard {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 20px;
}
.pcard-icon { font-size: 24px; margin-bottom: 10px; }
.pcard h3 { font-size: 15px; font-weight: 700; margin-bottom: 8px; color: #ffffff !important; }
.pcard p { font-size: 12px; color: #8fa3b8 !important; line-height: 1.5; }

/* Community Section */
.warm-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(0,192,127,0.08));
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 20px;
    padding: 30px;
    margin-top: 50px;
    text-align: center;
}

/* Form & UI Elements */
.stButton > button {
    background: #00C07F !important;
    color: #0d1b2a !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
    width: 100% !important;
    border: none !important;
    padding: 12px !important;
}

.ai-bubble {
    background: rgba(0,192,127,0.07);
    border: 1px solid rgba(0,192,127,0.18);
    border-radius: 12px;
    padding: 12px 16px;
    font-size: 13px;
    color: #ffffff !important;
    margin-bottom: 24px;
}

/* Resultados */
.track-pill {
    display: inline-block;
    background: rgba(0,192,127,0.12);
    border: 2px solid #00C07F;
    color: #00C07F !important;
    padding: 5px 16px;
    border-radius: 20px;
    text-transform: uppercase;
    font-size: 12px;
    font-weight: 800;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ── 3. LÓGICA DE IA (GROQ) ──────────────────────────────────────
def call_groq(name, interest, goal, strength, timeline):
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        st.error("⚠️ Falta GROQ_API_KEY en los Secrets.")
        st.stop()
    client = Groq(api_key=api_key)
    
    prompt = f"Genera un roadmap JSON para {name}. Interés: {interest}, Meta: {goal}, Fortaleza: {strength}, Tiempo: {timeline}."
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Eres la IA de FemPath. Responde solo con JSON válido."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# ── 4. ESTRUCTURA DE LA APLICACIÓN ──────────────────────────────
def main():
    if "result" not in st.session_state: st.session_state.result = None

    # HEADER (Restaurado de fempath.html)
    st.markdown('<div class="hero-tag">🚀 MAD Fellows Challenge 2026 · EPIC Lab ITAM</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">El <span class="hl">co-piloto de AI</span> para tu carrera en Tech & VC</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8fa3b8; font-size:17px; margin-bottom:40px;">FemPath te ayuda a navegar el ecosistema emprendedor con rutas personalizadas generadas por IA.</p>', unsafe_allow_html=True)

    # STATS ROW
    st.markdown("""
    <div class="stat-row">
      <div class="stat-box"><div class="stat-num">15%</div><div class="stat-lbl">Capital VC a startups de mujeres</div></div>
      <div class="stat-box"><div class="stat-num">52¢</div><div class="stat-lbl">Por cada peso que recibe un hombre</div></div>
      <div class="stat-box"><div class="stat-num">10%</div><div class="stat-lbl">Deal flow femenino en México</div></div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.result:
        # RESULTADOS
        res = st.session_state.result
        st.balloons()
        st.markdown(f'<div class="track-pill">{res.get("track_name", "Tu Ruta")}</div>', unsafe_allow_html=True)
        st.markdown(f"## {res.get('track_icon', '🚀')} {res.get('title', 'Plan de Acción')}")
        
        st.markdown(f'<div class="ai-bubble">🤖 <strong>Insight:</strong> {res.get("insight", "Listo para empezar.")}</div>', unsafe_allow_html=True)
        
        st.subheader("🔥 Acciones para esta semana")
        for act in res.get('week_actions', []):
            with st.expander(f"📌 {act['title']}"):
                st.write(act['detail'])
                st.caption(f"Acción: {act['cta']}")
        
        if st.button("↩ Crear otra ruta"):
            st.session_state.result = None
            st.rerun()
    else:
        # SECCIÓN EL PROBLEMA (Forzando visibilidad)
        st.markdown('<div style="text-transform:uppercase; color:#00C07F; font-size:11px; font-weight:700; letter-spacing:2px; margin-bottom:10px;">El Problema</div>', unsafe_allow_html=True)
        st.markdown('<h2 style="color:white !important;">¿Por qué hay tan pocas mujeres en Tech?</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="problem-grid">
          <div class="pcard">
            <div class="pcard-icon">🧠</div>
            <h3>Confidence Gap</h3>
            <p>Las mujeres suelen aplicar a roles solo si cumplen el 100% de los requisitos.</p>
          </div>
          <div class="pcard">
            <div class="pcard-icon">🤝</div>
            <h3>Network Access</h3>
            <p>Falta de acceso a redes de contacto y mentoras en etapas tempranas.</p>
          </div>
          <div class="pcard">
            <div class="pcard-icon">💰</div>
            <h3>Capital Bias</h3>
            <p>Sesgos inconscientes en la asignación de capital semilla y venture capital.</p>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # QUIZ
        st.markdown('<div style="background: rgba(255,255,255,0.03); padding: 30px; border-radius: 20px; border: 1px solid rgba(0,192,127,0.2);">', unsafe_allow_html=True)
        with st.form("quiz_form"):
            st.markdown('<h3 style="margin-top:0;">🤖 AI Pathfinder</h3>', unsafe_allow_html=True)
            name = st.text_input("¿Cómo te llamas?")
            interest = st.selectbox("Área de interés", ["Venture Capital", "Fintech", "Sostenibilidad", "Estrategia"])
            goal = st.selectbox("Tu meta a 5 años", ["Fundadora", "Inversionista", "Líder en Tech"])
            strength = st.selectbox("Tu mayor fortaleza", ["Análisis de Datos", "Networking", "Creatividad"])
            timeline = st.selectbox("¿Cuándo quieres empezar?", ["Ahora mismo", "Al graduarme"])
            
            submit = st.form_submit_button("✨ Generar Roadmap con Groq AI")
            if submit:
                if name:
                    with st.spinner("Analizando perfil..."):
                        try:
                            st.session_state.result = call_groq(name, interest, goal, strength, timeline)
                            st.rerun()
                        except Exception as e: st.error(f"Error: {e}")
                else: st.warning("Escribe tu nombre.")
        st.markdown('</div>', unsafe_allow_html=True)

    # COMMUNITY SECTION
    st.markdown("""
    <div class="warm-card">
      <div style="font-size:11px; font-weight:700; color:#00C07F; margin-bottom:10px; text-transform:uppercase;">Community & Network</div>
      <h2 style="color:white !important; margin-bottom:15px;">No camines sola</h2>
      <p style="color:#8fa3b8; margin-bottom:20px;">Únete a la comunidad de mujeres del EPIC Lab y conecta con mentoras que ya han recorrido el camino.</p>
      <div style="text-align:center;">
        <span style="background:#00C07F; color:#0d1b2a; padding:10px 25px; border-radius:8px; font-weight:800; cursor:pointer;">Próximamente</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # FOOTER
    st.markdown('<div style="text-align:center; margin-top:50px; color:#8fa3b8; font-size:12px;">FemPath · MAD Fellows 2026 · EPIC Lab ITAM</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
