import streamlit as st
from groq import Groq
import json

# ── 1. CONFIGURACIÓN Y ESTILO ────────────────────────────────
st.set_page_config(page_title="FemPath — AI Co-Pilot", page_icon="🚀", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    html, body, [class*="css"], .stApp {
        background-color: #0d1b2a !important;
        font-family: 'Inter', sans-serif;
        color: #ffffff !important;
    }
    .hero-tag {
        background: rgba(0,192,127,0.1); border: 1px solid rgba(0,192,127,0.3);
        color: #00C07F !important; padding: 6px 16px; border-radius: 20px;
        font-size: 13px; font-weight: 700; display: inline-block; margin-bottom: 20px;
    }
    .hl { color: #00C07F !important; font-weight: 900; }
    .ai-bubble {
        background: rgba(0,192,127,0.07); border: 1px solid rgba(0,192,127,0.18);
        border-radius: 12px; padding: 20px; margin: 20px 0; border-left: 5px solid #00C07F;
    }
    .stButton > button {
        background: #00C07F !important; color: #0d1b2a !important;
        font-weight: 800 !important; border-radius: 12px !important;
        width: 100% !important; border: none !important; height: 50px;
    }
</style>
""", unsafe_allow_html=True)

# ── 2. LLAMADA A LA IA ───────────────────────────────────────
def call_fempath_ai(name, interest, goal, strength, timeline):
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        st.error("🔑 Error: No configuraste 'GROQ_API_KEY' en los Secrets.")
        return None

    client = Groq(api_key=api_key)
    
    # El prompt ahora es súper estricto con los nombres de las llaves
    prompt = f"""
    Eres la IA de FemPath para el EPIC Lab ITAM. Crea un plan para {name}.
    Interés: {interest}, Meta: {goal}, Fortaleza: {strength}, Tiempo: {timeline}.
    
    RESPONDE EXCLUSIVAMENTE CON ESTE JSON:
    {{
      "res_titulo": "Título del Plan",
      "res_emoji": "🚀",
      "res_insight": "Breve consejo potente",
      "res_acciones": [
        {{"paso": "Paso 1", "detalle": "Qué hacer específicamente"}},
        {{"paso": "Paso 2", "detalle": "Qué hacer específicamente"}},
        {{"paso": "Paso 3", "detalle": "Qué hacer específicamente"}}
      ],
      "res_roadmap": ["Fase 1", "Fase 2", "Fase 3"]
    }}
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return json.loads(completion.choices[0].message.content)

# ── 3. LÓGICA DE NAVEGACIÓN ──────────────────────────────────
if "resultado_ai" not in st.session_state:
    st.session_state.resultado_ai = None

st.markdown('<div class="hero-tag">🚀 MAD Fellows 2026 · EPIC Lab ITAM</div>', unsafe_allow_html=True)
st.markdown('<h1>FemPath: Tu <span class="hl">Plan de Acción</span></h1>', unsafe_allow_html=True)

# VISTA DE RESULTADOS
if st.session_state.resultado_ai:
    res = st.session_state.resultado_ai
    st.balloons()
    
    # Aquí usamos .get('llave', 'texto_si_falla') para que NUNCA salga vacío
    titulo = res.get('res_titulo', 'Tu Ruta al Éxito')
    emoji = res.get('res_emoji', '✨')
    
    st.markdown(f"## {emoji} {titulo}")
    
    st.markdown(f"""
    <div class="ai-bubble">
        <h4 style='margin-top:0; color:#00C07F;'>🤖 Insight de la IA para {nombre if 'nombre' in locals() else 'ti'}</h4>
        <p style='margin-bottom:0;'>{res.get('res_insight', 'El primer paso es el más importante. ¡Empieza hoy!')}</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔥 Acciones para esta semana")
    # Buscamos la lista de acciones. Si no existe, usamos una vacía [].
    for item in res.get('res_acciones', []):
        with st.expander(f"📍 {item.get('paso', 'Acción Recomendada')}"):
            st.write(item.get('detalle', 'La IA está procesando los detalles, pero el enfoque es tu crecimiento en el sector.'))

    st.subheader("🗺️ Roadmap Estratégico")
    for step in res.get('res_roadmap', []):
        st.write(f"✅ {step}")

    if st.button("↩️ Crear nuevo perfil"):
        st.session_state.resultado_ai = None
        st.rerun()

# VISTA DE FORMULARIO
else:
    with st.form("main_form"):
        st.markdown("### 🤖 Genera tu ruta personalizada")
        nombre = st.text_input("¿Cómo te llamas?")
        area = st.selectbox("Área", ["Venture Capital", "Software & IA", "Fintech"])
        meta = st.selectbox("Meta", ["Fundadora", "Inversionista", "Directiva"])
        fuerza = st.selectbox("Habilidad", ["Análisis", "Networking", "Creatividad"])
        tiempo = st.selectbox("Cuándo", ["Inmediatamente", "Al graduarme"])
        
        btn = st.form_submit_button("✨ GENERAR MI PLAN")

        if btn:
            if not nombre:
                st.warning("Escribe tu nombre.")
            else:
                with st.spinner("🚀 Consultando a Llama 3..."):
                    resultado = call_fempath_ai(nombre, area, meta, fuerza, tiempo)
                    if resultado:
                        st.session_state.resultado_ai = resultado
                        st.rerun()

st.markdown('<div style="text-align:center; margin-top:50px; color:#8fa3b8; font-size:12px;">FemPath · MAD Fellows Challenge 2026</div>', unsafe_allow_html=True)
