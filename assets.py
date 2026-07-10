import streamlit as st
import random

def cargar_estilos():
    st.markdown("""
    <style>
        .stApp {
            background-color: #000000 !important;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(0, 229, 255, 0.05) 0%, transparent 45%),
                radial-gradient(circle at 75% 70%, rgba(156, 39, 176, 0.06) 0%, transparent 50%);
            background-attachment: fixed;
        }
        .main-title { text-align: center; color: #ffffff; font-size: 3.8rem; font-weight: 800; margin-bottom: 0px; }
        .main-title-suffix { font-weight: 300; animation: pulso-neon 2.5s infinite ease-in-out; }
        
        @keyframes pulso-neon {
            0%, 100% { text-shadow: 0 0 5px #00e5ff; color: #00e5ff; }
            50% { text-shadow: 0 0 21px #00e5ff; color: #ffffff; }
        }
        
        /* Contenedores con espaciados de Fibonacci (Margen: 21px, Radio: 13px) */
        .lab-panel { 
            background-color: rgba(15, 23, 42, 0.55) !important; 
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-left: 5px solid #00e5ff !important; 
            padding: 34px; 
            border-radius: 13px; 
            margin-bottom: 21px; 
            backdrop-filter: blur(13px);
        }
        
        /* Botonera Neón con Proporción Áurea (Padding vertical: 13px, Horizontal: 34px) */
        .stButton>button {
            background: rgba(0, 229, 255, 0.03) !important;
            color: #00e5ff !important;
            border: 1px solid rgba(0, 229, 255, 0.35) !important;
            border-radius: 8px !important;
            padding: 13px 34px !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
        }
        .stButton>button:hover {
            background: rgba(0, 229, 255, 0.15) !important;
            border-color: #00e5ff !important;
            box-shadow: 0 0 21px rgba(0, 229, 255, 0.6) !important;
        }
        .card-success { border-left: 5px solid #4caf50; padding: 21px; background: rgba(76,175,80,0.05); margin-top: 13px; }
        .card-error { border-left: 5px solid #f44336; padding: 21px; background: rgba(244,67,54,0.05); margin-top: 13px; }
        .card-hint { border-left: 5px solid #ffb142; padding: 21px; background: rgba(255,177,66,0.05); margin-top: 13px; }
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
