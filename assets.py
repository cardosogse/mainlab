import streamlit as st
import random

def cargar_estilos():
    st.markdown("""
    <style>
        /* Fondo Universo: Negro Absoluto */
        .stApp {
            background-color: #000000 !important;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(0, 229, 255, 0.05) 0%, transparent 45%),
                radial-gradient(circle at 75% 70%, rgba(156, 39, 176, 0.06) 0%, transparent 50%),
                radial-gradient(white 1px, transparent 1px),
                radial-gradient(white 1.5px, transparent 1.5px);
            background-size: 100% 100%, 100% 100%, 250px 250px, 160px 150px;
            background-attachment: fixed;
        }
        .main-title { text-align: center; color: #ffffff; font-size: 3.8rem; font-weight: 800; margin-bottom: 0px; letter-spacing: 2px; text-shadow: 0 0 15px rgba(255,255,255,0.1); }
        
        /* Paneles Glassmorphism */
        .lab-panel { 
            background-color: rgba(15, 23, 42, 0.55) !important; 
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-left: 5px solid #00e5ff !important; 
            padding: 22px; 
            border-radius: 12px; 
            margin-bottom: 20px; 
            backdrop-filter: blur(12px);
        }
        
        /* BLINDAJE DE PRIVACIDAD TOTAL */
        #MainMenu, footer, header { visibility: hidden !important; display: none !important; }
        [data-testid="stDecoration"], [data-testid="stToolbar"], [data-testid="stStatusWidget"] { visibility: hidden !important; display: none !important; }
        .st-emotion-cache-12fm652, .st-emotion-cache-1avcm0n { visibility: hidden !important; display: none !important; }
    </style>
    """, unsafe_allow_html=True)

def obtener_svg_atomo(modelo_nombre):
    if "Dalton" in modelo_nombre:
        return "<svg viewBox='0 0 100 100' width='90' height='90'><circle cx='50' cy='50' r='34' fill='none' stroke='#90a4ae' stroke-width='2.5'/><circle cx='50' cy='50' r='31' fill='#90a4ae' opacity='0.15'/></svg>"
    elif "Thomson" in modelo_nombre:
        return "<svg viewBox='0 0 100 100' width='90' height='90'><circle cx='50' cy='50' r='34' fill='#9c27b0' opacity='0.15' stroke='#9c27b0' stroke-width='1.5'/><circle cx='34' cy='38' r='4' fill='#ffffff'/><text x='32' y='41' fill='black' font-size='9' font-weight='bold'>-</text><circle cx='66' cy='42' r='4' fill='#ffffff'/><text x='64' y='45' fill='black' font-size='9' font-weight='bold'>-</text><circle cx='48' cy='68' r='4' fill='#ffffff'/><text x='46' y='71' fill='black' font-size='9' font-weight='bold'>-</text><text x='45' y='54' fill='#9c27b0' font-size='14' font-weight='bold'>+</text></svg>"
    elif "Rutherford" in modelo_nombre:
        return "<svg viewBox='0 0 100 100' width='90' height='90'><circle cx='50' cy='50' r='6' fill='#2196f3'/><text x='47' y='54' fill='white' font-size='9' font-weight='bold'>+</text><ellipse cx='50' cy='50' rx='38' ry='10' fill='none' stroke='#2196f3' stroke-width='1' opacity='0.6' transform='rotate(30 50 50)'/><ellipse cx='50' cy='50' rx='38' ry='10' fill='none' stroke='#2196f3' stroke-width='1' opacity='0.6' transform='rotate(-30 50 50)'/><circle cx='22' cy='34' r='2.5' fill='#ffffff'/><circle cx='78' cy='66' r='2.5' fill='#ffffff'/></svg>"
    elif "Bohr" in modelo_nombre:
        return "<svg viewBox='0 0 100 100' width='90' height='90'><circle cx='50' cy='50' r='7' fill='#ffb142'/><circle cx='50' cy='50' r='20' fill='none' stroke='#ffb142' stroke-width='1' stroke-dasharray='2 2'/><circle cx='50' cy='50' r='36' fill='none' stroke='#ffb142' stroke-width='1'/><circle cx='50' cy='14' r='3' fill='#ffffff'/><circle cx='68' cy='38' r='3' fill='#ffffff'/></svg>"
    else:
        return "<svg viewBox='0 0 100 100' width='90' height='90'><defs><radialGradient id='cloud' cx='50%' cy='50%' r='50%'><stop offset='0%' stop-color='#00e5ff' stop-opacity='0.8'/><stop offset='50%' stop-color='#00e5ff' stop-opacity='0.25'/><stop offset='100%' stop-color='#00e5ff' stop-opacity='0'/></radialGradient></defs><circle cx='50' cy='50' r='38' fill='url(#cloud)'/><circle cx='50' cy='4' fill='#ffffff'/></svg>"

ELEMENTOS = {
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "sym": "C"},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "sym": "H"},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "sym": "O"},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "sym": "N"},
    "Fósforo (P)": {"fuerza": 2.19, "color": "#ff7ff5", "sym": "P"},
    "Azufre (S)": {"fuerza": 2.58, "color": "#ffda79", "sym": "S"}
}

def generar_svg_enlace(sym1, f1, c1, sym2, f2, c2):
    diff = abs(f1 - f2)
    if diff == 0: cx_e1, cx_e2, ellipse_x, stroke_color, stroke_dash = 113, 127, 120, "#ffffff", "2 2"
    elif diff > 0.4: cx_e1, cx_e2, ellipse_x, stroke_color, stroke_dash = (85, 95, 100, c1, "4 2") if f1 > f2 else (145, 155, 140, c2, "4 2")
    else: cx_e1, cx_e2, ellipse_x, stroke_color, stroke_dash = 105, 135, 120, "#b0bec5", "3 3"
    return f"<div style='display:flex; justify-content:center; align-items:center; width:100%; height:130px;'><svg viewBox='0 0 240 120' width='100%' height='100%'><circle cx='70' cy='60' r='22' fill='{c1}' opacity='0.85'/><text x='64' y='65' fill='black' font-weight='bold' font-size='14'>{sym1}</text><circle cx='170' cy='60' r='18' fill='{c2}' opacity='0.85'/><text x='164' y='64' fill='black' font-weight='bold' font-size='12'>{sym2}</text><ellipse cx='{ellipse_x}' cy='60' rx='68' ry='32' fill='none' stroke='{stroke_color}' stroke-width='1.5' stroke-dasharray='{stroke_dash}'/><circle cx='{cx_e1}' cy='60' r='4' fill='#ffffff'/><circle cx='{cx_e2}' cy='60' r='4' fill='#ffffff'/></svg></div>"

def mezclar_memorama():
    contenido = [
        ("Dalton (1810)", 1), ("Materia indivisible sin cargas", 1),
        ("Thomson (1897)", 2), ("Esfera positiva con electrones incrustados", 2),
        ("Rutherford (1911)", 3), ("Núcleo denso positivo y espacio vacío", 3),
        ("Bohr (1913)", 4), ("Órbitas circulares planas cuantizadas", 4),
        ("Schrödinger (1926)", 5), ("Orbitales 3D (Flexibilidad cuántica)", 5)
    ]
    random.shuffle(contenido)
    return contenido
