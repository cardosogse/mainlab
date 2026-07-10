import streamlit as st
import random

# DEFINICIÓN GLOBAL MAESTRA - Evita el ImportError en m1_dia3.py
ELEMENTOS = {
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "sym": "C"},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "sym": "H"},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "sym": "O"},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "sym": "N"},
    "Fósforo (P)": {"fuerza": 2.19, "color": "#ff7ff5", "sym": "P"},
    "Azufre (S)": {"fuerza": 2.58, "color": "#ffda79", "sym": "S"},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "sym": "O"},
    "Sodio (Na)": {"fuerza": 0.93, "color": "#00e5ff", "sym": "Na"},
    "Cloro (Cl)": {"fuerza": 3.16, "color": "#ffb142", "sym": "Cl"}
}

def cargar_estilos():
    st.markdown("""
    <style>
        /* Fondo Universo: Negro Absoluto + Nebulosas de polvo cósmico */
        .stApp {
            background-color: #000000 !important;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(0, 229, 255, 0.06) 0%, transparent 45%),
                radial-gradient(circle at 75% 70%, rgba(156, 39, 176, 0.07) 0%, transparent 50%),
                radial-gradient(white 1px, transparent 1px),
                radial-gradient(white 1.5px, transparent 1.5px);
            background-size: 100% 100%, 100% 100%, 250px 250px, 160px 150px;
            background-position: 0 0, 0 0, 0 0, 40px 60px;
            background-attachment: fixed;
        }
        .main-title { text-align: center; color: #ffffff; font-size: 3.8rem; font-weight: 800; margin-bottom: 0px; letter-spacing: 2px; }
        .main-title-suffix { font-weight: 300; animation: pulso-neon 2.5s infinite ease-in-out; }
        
        @keyframes pulso-neon {
            0%, 100% { text-shadow: 0 0 5px #00e5ff, 0 0 10px #00e5ff; color: #00e5ff; }
            50% { text-shadow: 0 0 21px #00e5ff, 0 0 34px #00e5ff; color: #ffffff; }
        }
        
        /* Contenedores con espaciados basados en Fibonacci (Margen: 21px, Radio: 13px, Padding: 34px) */
        .lab-panel { 
            background-color: rgba(15, 23, 42, 0.65) !important; 
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-left: 5px solid #00e5ff !important; 
            padding: 34px; 
            border-radius: 13px; 
            margin-bottom: 21px; 
            backdrop-filter: blur(13px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        }
        
        /* Botones Neón Estilizados con Proporción Áurea (Padding: 13px vertical, 34px horizontal) */
        .stButton>button {
            background: rgba(0, 229, 255, 0.03) !important;
            color: #00e5ff !important;
            border: 1px solid rgba(0, 229, 255, 0.35) !important;
            border-radius: 8px !important;
            padding: 13px 34px !important;
            font-weight: bold !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .stButton>button:hover {
            background: rgba(0, 229, 255, 0.18) !important;
            border-color: #00e5ff !important;
            color: #ffffff !important;
            box-shadow: 0 0 21px rgba(0, 229, 255, 0.6) !important;
        }
        .card-success { border-left: 5px solid #4caf50; padding: 21px; background: rgba(76,175,80,0.05); margin-top: 13px; border-radius: 8px; }
        .card-error { border-left: 5px solid #f44336; padding: 21px; background: rgba(244,67,54,0.05); margin-top: 13px; border-radius: 8px; }
        .card-hint { border-left: 5px solid #ffb142; padding: 21px; background: rgba(255,177,66,0.05); margin-top: 13px; color: #ffda79; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

def obtener_svg_atomo(modelo_nombre):
    if "Dalton" in modelo_nombre:
        return "<svg viewBox='0 0 100 100' width='90' height='90'><circle cx='50' cy='50' r='34' fill='none' stroke='#90a4ae' stroke-width='2.5'/></svg>"
    elif "Thomson" in modelo_nombre:
        return "<svg viewBox='0 0 100 100' width='90' height='90'><circle cx='50' cy='50' r='34' fill='#9c27b0' opacity='0.15'/><text x='45' y='55' fill='#9c27b0'>+</text></svg>"
    elif "Rutherford" in modelo_nombre:
        return "<svg viewBox='0 0 100 100' width='90' height='90'><circle cx='50' cy='50' r='6' fill='#2196f3'/><ellipse cx='50' cy='50' rx='34' ry='10' fill='none' stroke='#2196f3' transform='rotate(30 50 50)'/></svg>"
    elif "Bohr" in modelo_nombre:
        return "<svg viewBox='0 0 100 100' width='90' height='90'><circle cx='50' cy='50' r='7' fill='#ffb142'/><circle cx='50' cy='50' r='20' fill='none' stroke='#ffb142' stroke-dasharray='2 2'/></svg>"
    else:
        return "<svg viewBox='0 0 100 100' width='90' height='90'><circle cx='50' cy='50' r='34' fill='#00e5ff' opacity='0.25'/></svg>"

def generar_svg_enlace(sym1, f1, c1, sym2, f2, c2):
    diff = abs(f1 - f2)
    ellipse_x = 100 if f1 > f2 else (140 if f2 > f1 else 120)
    return f"""<div style='display:flex; justify-content:center; align-items:center; width:100%; height:130px;'>
        <svg viewBox='0 0 240 120' width='100%' height='100%'>
            <circle cx='70' cy='60' r='22' fill='{c1}' opacity='0.85'/>
            <text x='64' y='65' fill='black' font-weight='bold'>{sym1}</text>
            <circle cx='170' cy='60' r='18' fill='{c2}' opacity='0.85'/>
            <text x='164' y='64' fill='black' font-weight='bold'>{sym2}</text>
            <ellipse cx='{ellipse_x}' cy='60' rx='68' ry='32' fill='none' stroke='#ffffff' stroke-width='1.5' stroke-dasharray='3 3'/>
        </svg>
    </div>"""

def mezclar_memorama():
    contenido = [
        ("Dalton (1810)", 1), ("Materia indivisible sin cargas", 1),
        ("Thomson (1897)", 2), ("Esfera positiva con electrones", 2),
        ("Rutherford (1911)", 3), ("Núcleo denso positivo", 3),
        ("Bohr (1913)", 4), ("Órbitas circulares cuantizadas", 4),
        ("Schrödinger (1926)", 5), ("Orbitales de densidad 3D", 5)
    ]
    random.shuffle(contenido)
    return contenido
