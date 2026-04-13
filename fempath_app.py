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

# ── DISEÑO CSS PERSONALIZADO (Corregido) ─────────────────────
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
.stButton > button {
    background: #00C07F !important;
    color: #0d1b2a !important;
    font-weight: 800 !important;
