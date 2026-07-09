import streamlit as st
import random

def cargar_estilos():
    # Estilos CSS con escudo de privacidad inyectado
    st.markdown("""
    <style>
        .stApp { background-color: #000000 !important; }
        .main-title { text-align: center; color: #ffffff; font-size: 3.8rem; font-weight: 800; margin-bottom: 0px; }
        .lab-panel { background-color: rgba(15, 23, 42, 0.55) !important; border: 1px solid rgba(255, 255, 255, 0.08) !important; border-left: 5px solid #00e5ff !important; padding: 22px; border-radius: 12px; margin-bottom: 20px; backdrop-filter: blur(12px); }
        
        /* ESCUDO DE PRIVACIDAD TOTAL */
        #MainMenu, footer, header { visibility: hidden !important; display: none !important; }
        [data-testid="stDecoration"], [data-testid="stToolbar"], [data-testid="stStatusWidget"] { visibility: hidden !important; display: none !important; }
        .st-emotion-cache-12fm652, .st-emotion-cache-1avcm0n { visibility: hidden !important; display: none !important; }
    </style>
    """, unsafe_allow_html=True)

def obtener_svg_atomo(modelo_nombre):
    return "<svg viewBox='0 0 100 100' width='90' height='90'><circle cx='50' cy='50' r='38' fill='#00e5ff'/></svg>"

ELEMENTOS = {
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "sym": "C"},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "sym": "H"},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "sym": "O"}
}

def generar_svg_enlace(sym1, f1, c1, sym2, f2, c2):
    return "<svg></svg>"

def mezclar_memorama():
    return [("Dalton", 1), ("Thomson", 2)]
