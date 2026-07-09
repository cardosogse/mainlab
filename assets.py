import streamlit as st
import random

def cargar_estilos():
    st.markdown("""
    <style>
        /* Fondo Universo: Negro Absoluto + Galaxias / Nebulosas de polvo cósmico */
        .stApp {
            background-color: #000000 !important;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(0, 229, 255, 0.05) 0%, transparent 45%),
                radial-gradient(circle at 75% 70%, rgba(156, 39, 176, 0.06) 0%, transparent 50%),
                radial-gradient(white 1px, transparent 1px),
                radial-gradient(white 1.5px, transparent 1.5px);
            background-size: 100% 100%, 100% 100%, 250px 250px, 160px 150px;
            background-position: 0 0, 0 0, 0 0, 40px 60px;
            background-attachment: fixed;
        }
        .main-title { text-align: center; color: #ffffff; font-size: 3.8rem; font-weight: 800; margin-bottom: 0px; letter-spacing: 2px; text-shadow: 0 0 15px rgba(255,255,255,0.1); }
        
        /* 🌌 Efecto de pulsación neón / radiactiva orgánica para el logotipo */
        @keyframes pulso-neon {
            0% { text-shadow: 0 0 5px #00e5ff, 0 0 10px #00e5ff; color: #00e5ff; opacity: 0.8; }
            50% { text-shadow: 0 0 20px #00e5ff, 0 0 30px #00e5ff, 0 0 40px #00e5ff; color: #ffffff; opacity: 1; }
            100% { text-shadow: 0 0 5px #00e5ff, 0 0 10px #00e5ff; color: #00e5ff; opacity: 0.8; }
        }
        .main-title-suffix { font-weight: 300; animation: pulso-neon 2.5s infinite ease-in-out; }
        .sub-title { text-align: center; font-style: italic; color: #90a4ae; font-size: 1.2rem; margin-top: 5px; margin-bottom: 30px; }
        
        /* Paneles Traslúcidos de Alta Tecnología (Glassmorphism Premium) */
        .lab-panel { 
            background-color: rgba(15, 23, 42, 0.55) !important; 
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-left: 5px solid #00e5ff !important; 
            padding: 22px; 
            border-radius: 12px; 
            margin-bottom: 20px; 
            backdrop-filter: blur(12px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
        }
        .card-success { background-color: rgba(76, 175, 80, 0.08); border: 1px solid rgba(76, 175, 80, 0.2); border-left: 5px solid #4caf50; padding: 15px; border-radius: 6px; margin-top: 10px; }
        .card-error { background-color: rgba(244, 67, 54, 0.08); border: 1px solid rgba(244, 67, 54, 0.2); border-left: 5px solid #f44336; padding: 15px; border-radius: 6px; margin-top: 10px; }
        .card-hint { background-color: rgba(255, 177, 66, 0.08); border: 1px solid rgba(255, 177, 66, 0.2); border-left: 5px solid #ffb142; padding: 15px; border-radius: 6px; margin-top: 10px; color: #ffda79;}
        .monitor-box { background-color: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 12px; border-radius: 6px; text-align: center; margin-bottom: 10px;}
        
        /* Optimización de Botonera Neón de Alta Reactividad */
        .stButton>button {
            background: rgba(0, 229, 255, 0.03) !important;
            color: #00e5ff !important;
            border: 1px solid rgba(0, 229, 255, 0.35) !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: bold !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .stButton>button:hover {
            background: rgba(0, 229, 255, 0.15) !important;
            border-color: #00e5ff !important;
            color: #ffffff !important;
            box-shadow: 0 0 20px rgba(0, 229, 255, 0.6), inset 0 0 8px rgba(0, 229, 255, 0.3) !important;
            transform: translateY(-1px);
        }
        .stButton>button:active {
            transform: translateY(1px);
        }

        /* Estilizado de pestañas de navegación */
        .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
        .stTabs [data-baseweb="tab"] { background-color: rgba(255,255,255,0.03); border-radius: 4px 4px 0 0; padding: 10px 20px; color: #90a4ae; font-weight: bold; }
        .stTabs [aria-selected="true"] { background-color: rgba(0, 229, 255, 0.12) !important; color: #00e5ff !important; border-bottom: 2px solid #00e5ff !important; }
        
        /* Subnavegación del Radio Horizontal */
        div[data-testid="stRadio"] > div{ flex-direction: row !important; gap: 12px !important; flex-wrap: wrap; }
        div[data-testid="stRadio"] label {
            background-color: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            padding: 10px 18px !important;
            border-radius: 20px !important;
            color: #cfd8dc !important;
            transition: all 0.2s ease-in-out !important;
            cursor: pointer !important;
        }
        div[data-testid="stRadio"] label:hover {
            background-color: rgba(0, 229, 255, 0.08) !important;
            border-color: #00e5ff !important;
            color: #ffffff !important;
            box-shadow: 0 0 10px rgba(0, 229, 255, 0.3);
        }
        div[data-testid="stRadio"] label[data-checked="true"] {
            background-color: rgba(0, 229, 255, 0.16) !important;
            border-color: #00e5ff !important;
            color: #00e5ff !important;
            font-weight: bold !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child { display: none !important; }

        @keyframes parpadeoPulso {
            0% { opacity: 0.3; text-shadow: 0 0 0px transparent; }
            50% { opacity: 1; text-shadow: 0 0 8px #ffb142; }
            100% { opacity: 0.3; text-shadow: 0 0 0px transparent; }
        }
        .foco-parpadeante { animation: parpadeoPulso 2.5s infinite ease-in-out; color: #ffb142; font-weight: bold; display: inline-block; }

        .card-dalton { background-color: rgba(144, 164, 174, 0.06); border: 1px solid rgba(144, 164, 174, 0.2); border-left: 5px solid #90a4ae; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
        .card-thomson { background-color: rgba(156, 39, 176, 0.06); border: 1px solid rgba(156, 39, 176, 0.2); border-left: 5px solid #9c27b0; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
        .card-rutherford { background-color: rgba(33, 150, 243, 0.06); border: 1px solid rgba(33, 150, 243, 0.2); border-left: 5px solid #2196f3; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
        .card-bohr { background-color: rgba(255, 177, 66, 0.06); border: 1px solid rgba(255, 177, 66, 0.2); border-left: 5px solid #ffb142; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
        .card-schrodinger { background-color: rgba(0, 229, 255, 0.06); border: 1px solid rgba(0, 229, 255, 0.2); border-left: 5px solid #00e5ff; padding: 20px; border-radius: 6px; margin-bottom: 15px; }
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

def generar_svg_tira_afloja(f1, c1, sym1, f2, c2, sym2):
    diff = abs(f1 - f2)
    cx_e = 120 if f1 == f2 else (80 + (1.0 / diff) * 5 if f1 > f2 else 160 - (1.0 / diff) * 5)
    stroke_color = "#ffffff" if f1 == f2 else (c1 if f1 > f2 else c2)
    return f"<div style='display:flex; justify-content:center; align-items:center; width:100%; height:120px;'><svg viewBox='0 0 240 100' width='100%' height='100%'><line x1='60' y1='50' x2='180' y2='50' stroke='#555' stroke-width='2' stroke-dasharray='4 4'/><circle cx='60' cy='50' r='22' fill='{c1}' opacity='0.85'/><text x='54' y='55' fill='black' font-weight='bold' font-size='14'>{sym1}</text><text x='15' y='92' fill='#cfd8dc' font-size='11'>Val: {f1}</text><circle cx='180' cy='50' r='22' fill='{c2}' opacity='0.85'/><text x='174' y='55' fill='black' font-weight='bold' font-size='14'>{sym2}</text><text x='150' y='92' fill='#cfd8dc' font-size='11'>Val: {f2}</text><ellipse cx='{cx_e}' cy='50' rx='55' ry='28' fill='none' stroke='{stroke_color}' stroke-width='1.8' stroke-dasharray='3 1'/><circle cx='{cx_e}' cy='50' r='6' fill='#00e5ff'/></svg></div>"

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
