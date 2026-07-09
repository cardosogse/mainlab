import streamlit as st
import random

def cargar_estilos():
    # 1. Estilos base del sistema y estética de "Universo"
    st.markdown("""
    <style>
        /* Fondo Universo: Negro Absoluto + Nebulosas */
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
        
        .main-title { 
            text-align: center; color: #ffffff; font-size: 3.8rem; font-weight: 800; 
            margin-bottom: 0px; letter-spacing: 2px; text-shadow: 0 0 15px rgba(255,255,255,0.1); 
        }

        .lab-panel {
            background-color: #0f172a; padding: 20px; border-radius: 12px; 
            border: 1px solid #334155; margin-bottom: 15px;
        }

        /* 2. ESCUDO DE PRIVACIDAD: Oculta menús, footer y herramientas de desarrollo */
        #MainMenu, footer, header { 
            visibility: hidden !important; 
            display: none !important; 
        }
        
        [data-testid="stDecoration"], [data-testid="stToolbar"], [data-testid="stStatusWidget"] { 
            visibility: hidden !important; 
            display: none !important; 
        }
    </style>
    """, unsafe_allow_html=True)

# --- UTILIDADES ADICIONALES ---

def mezclar_memorama():
    # Genera los pares para el juego de memoria
    elementos = ["⚛️", "🧬", "🧪", "🔬", "🔋"] * 2
    random.shuffle(elementos)
    # Crea una lista de tuplas (emoji, ID único)
    return [(elementos[i], i) for i in range(10)]

def generar_svg_enlace(c1, sym1, c2, sym2, diff):
    # Función para visualizar enlaces moleculares
    # Nota: Mantenemos tu lógica de renderizado original
    cx_e1, cx_e2, ellipse_x, stroke_color, stroke_dash = 113, 127, 120, "#ffffff", "2 2"
    
    if diff > 0.4:
        # Lógica de enlace polar/iónico
        f1, f2 = 2.0, 2.0
        cx_e1, cx_e2, ellipse_x, stroke_color, stroke_dash = (85, 95, 100, c1, "4 2") if f1 > f2 else (145, 155, 140, c2, "4 2")
    elif diff == 0:
        cx_e1, cx_e2, ellipse_x, stroke_color, stroke_dash = 105, 135, 120, "#b0bec5", "3 3"
        
    return f"""
    <div style='display:flex; justify-content:center; align-items:center; width:100%; height:130px;'>
        <svg viewBox='0 0 240 120' width='100%' height='100%'>
            <circle cx='70' cy='60' r='22' fill='{c1}' opacity='0.85'/>
            <text x='64' y='65' fill='black' font-weight='bold' font-size='14'>{sym1}</text>
            <circle cx='170' cy='60' r='18' fill='{c2}' opacity='0.85'/>
            <text x='164' y='64' fill='black' font-weight='bold' font-size='12'>{sym2}</text>
            <ellipse cx='{ellipse_x}' cy='60' rx='40' ry='15' fill='transparent' stroke='{stroke_color}' stroke-dasharray='{stroke_dash}'/>
        </svg>
    </div>
    """
