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

# ── 2. ESTILOS CSS (Sincronizados con fempath.html) ─────────────
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

/* Hero & Tags */
.hero-tag {
    display: inline-block;
    background: rgba(0,192,127,0.1);
    border: 1px solid rgba(0,192,127,0.3);
    color: #00C07F;
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
}
.hero-title .hl { color: #00C07F; }

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
.stat-num { font-size: 32px; font-weight: 900; color: #00C07F; }
.stat-lbl { font-size: 11px; color: #8fa3b8; margin-top: 6px; }

/* Problem Cards (NUEVO de fempath.html) */
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
.pcard h3 { font-size: 15px; font-weight: 700; margin-bottom: 8px; }
.pcard p { font-size: 12px; color: #8fa3b8; line-height: 1.5; }

/* Community Section (NUEVO de fempath.html) */
.warm-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(0,192,127,0.08));
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 20px;
    padding: 30px;
    margin-top: 50px;
    text-align: center;
}

/* Form & Buttons */
.stButton > button {
    background: #00C07F !important;
    color: #0d1b2a !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
    width: 100% !important;
    border: none !important;
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

    # HERO SECTION (de fempath.html)
    st.markdown('<div class="hero-tag">🚀 MAD Fellows Challenge 2026 · EPIC Lab ITAM</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">El <span class="hl">co-piloto de AI</span> para tu carrera en Tech & VC</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#8fa3b8; font-size:17px;">FemPath te ayuda a navegar el ecosistema emprendedor con rutas personalizadas generadas por IA.</p>', unsafe_allow_html=True)

    # STATS ROW (de fempath.html)
    st.markdown("""
    <div class="stat-row">
      <div class="stat-box"><div class="stat-num">15%</div><div class="stat-lbl">Capital VC a startups de mujeres</div></div>
      <div class="stat-box"><div class="stat-num">52¢</div><div class="stat-lbl">Por cada peso que recibe un hombre</div></div>
      <div class="stat-box"><div class="stat-num">10%</div><div class="stat-lbl">Deal flow femenino en México</div></div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.result:
        # Renderizar resultados (Roadmap)
        res = st.session_state.result
        st.balloons()
        st.markdown(f"### {res.get('track_icon', '🚀')} {res.get('track_name', 'Tu Ruta')}")
        st.info(f"🤖 **Insight:** {res.get('insight', 'Prepárate para el éxito.')}")
        
        # Acciones de la semana
        for act in res.get('week_actions', []):
            with st.expander(f"📌 {act['title']}"):
                st.write(act['detail'])
        
        if st.button("↩ Crear otro perfil"):
            st.session_state.result = None
            st.rerun()
    else:
        # SECCIÓN DE PROBLEMA (Extraído de fempath.html)
        st.markdown('<div style="text-transform:uppercase; color:#00C07F; font-size:11px; font-weight:700; letter-spacing:2px; margin-bottom:10px;">El Problema</div>', unsafe_allow_html=True)
        st.markdown('<h2>¿Por qué hay tan pocas mujeres en Tech?</h2>', unsafe_allow_html=True)
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

        # FORMULARIO / QUIZ
        with st.form("quiz_path"):
            st.markdown("### 🤖 AI Pathfinder — Crea tu ruta personalizada")
            name = st.text_input("¿Cómo te llamas?")
            interest = st.selectbox("Interés", ["Venture Capital", "Fintech", "Sostenibilidad", "Estrategia"])
            goal = st.selectbox("Meta", ["Fundadora", "Inversionista", "Líder en Tech"])
            strength = st.selectbox("Fortaleza", ["Datos", "Networking", "Creatividad"])
            timeline = st.selectbox("Horizonte", ["Ahora mismo", "Al graduarme"])
            
            if st.form_submit_button("✨ Generar Roadmap con Groq AI"):
                if name:
                    with st.spinner("Analizando con Llama 3..."):
                        try:
                            st.session_state.result = call_groq(name, interest, goal, strength, timeline)
                            st.rerun()
                        except Exception as e: st.error(f"Error: {e}")
                else: st.warning("Por favor escribe tu nombre.")

    # SECCIÓN DE COMUNIDAD (Extraído de fempath.html)
    st.markdown("""
    <div class="warm-card">
      <div style="font-size:11px; font-weight:700; color:#00C07F; margin-bottom:10px;">COMMUNITY & NETWORK</div>
      <h2 style="font-size:28px; margin-bottom:15px;">No camines sola</h2>
      <p style="color:#8fa3b8; font-size:14px; margin-bottom:20px;">Únete a la comunidad de mujeres del EPIC Lab y conecta con mentoras que ya han recorrido el camino.</p>
      <div style="display:flex; justify-content:center; gap:10px;">
        <input type="email" placeholder="tu@email.com" style="padding:10px; border-radius:8px; border:1px solid #333; background:#122236; color:white;">
        <button style="background:#00C07F; border:none; padding:10px 20px; border-radius:8px; font-weight:700; cursor:pointer;">Unirme</button>
      </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
