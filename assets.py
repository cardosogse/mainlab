import streamlit as st
import random

# ==========================================
# CONFIGURACIÓN Y ESTRUCTURAS DE DATOS GLOBALES
# ==========================================

# Catálogo maestro de propiedades físicas y estéticas de los bioelementos esenciales
ELEMENTOS = {
    "Carbono (C)": {"fuerza": 2.55, "color": "#ffb142", "sym": "C"},
    "Hidrógeno (H)": {"fuerza": 2.20, "color": "#00e5ff", "sym": "H"},
    "Oxígeno (O)": {"fuerza": 3.44, "color": "#ff5252", "sym": "O"},
    "Nitrógeno (N)": {"fuerza": 3.04, "color": "#33d9b2", "sym": "N"},
    "Fósforo (P)": {"fuerza": 2.19, "color": "#ff7ff5", "sym": "P"},
    "Azufre (S)": {"fuerza": 2.58, "color": "#ffda79", "sym": "S"},
    "Sodio (Na)": {"fuerza": 0.93, "color": "#00e5ff", "sym": "Na"},
    "Cloro (Cl)": {"fuerza": 3.16, "color": "#ffb142", "sym": "Cl"}
}

# Diccionario de respaldo seguro para mitigar KeyErrors si se solicita un elemento inexistente
_FALLBACK_ELEMENTO = {"fuerza": 2.00, "color": "#ffffff", "sym": "X"}


# ==========================================
# INYECCIÓN DE ESTILOS CSS (UI/UX RESPONSIVO)
# ==========================================

def cargar_estilos():
    """
    Inyecta de forma segura el motor de estilos CSS personalizado en el frontend de Streamlit.
    Garantiza la consistencia visual del laboratorio digital en pantallas móviles y de escritorio.
    """
    st.markdown("""
    <style>
        /* Reconfiguración de la estructura del contenedor base de Streamlit */
        .stApp {
            background-color: #000000 !important;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(0, 229, 255, 0.05) 0%, transparent 45%),
                radial-gradient(circle at 75% 70%, rgba(156, 39, 176, 0.06) 0%, transparent 50%),
                radial-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
                radial-gradient(rgba(255, 255, 255, 0.08) 1.5px, transparent 1.5px);
            background-size: 100% 100%, 100% 100%, 250px 250px, 160px 150px;
            background-position: 0 0, 0 0, 0 0, 40px 60px;
            background-attachment: fixed;
        }
        
        /* Título Principal de la Aplicación */
        .main-title { 
            text-align: center !important; 
            color: #ffffff; 
            font-size: clamp(2.2rem, 5vw, 3.8rem); /* Tipografía adaptativa responsiva */
            font-weight: 800; 
            margin-bottom: 21px; 
            letter-spacing: 2px;
            display: block !important;
            width: 100% !important;
        }
        
        .main-title-suffix { 
            font-weight: 300; 
            animation: pulso-neon 3s infinite ease-in-out; 
        }
        
        @keyframes pulso-neon {
            0%, 100% { text-shadow: 0 0 8px #00e5ff, 0 0 15px #00e5ff; color: #00e5ff; }
            50% { text-shadow: 0 0 25px #00e5ff, 0 0 40px #00e5ff; color: #ffffff; }
        }
        
        /* Paneles contenedores de actividades lógicas */
        .lab-panel { 
            background-color: rgba(15, 23, 42, 0.65) !important; 
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-left: 5px solid #00e5ff !important; 
            padding: clamp(15px, 3vw, 34px); /* Espaciado interno dinámico para pantallas pequeñas */
            border-radius: 13px; 
            margin-bottom: 21px; 
            backdrop-filter: blur(13px);
            -webkit-backdrop-filter: blur(13px);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        }
        
        /* Customización avanzada de botones globales */
        .stButton>button {
            background: rgba(0, 229, 255, 0.02) !important;
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
            box-shadow: 0 0 20px rgba(0, 229, 255, 0.5) !important;
        }
        
        .stButton>button:disabled {
            background: rgba(255, 255, 255, 0.02) !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
            color: rgba(255, 255, 255, 0.2) !important;
            box-shadow: none !important;
        }
        
        /* Tarjetas de notificación informativa y diagnóstico clínico */
        .card-success { border-left: 5px solid #4caf50; padding: 18px; background: rgba(76,175,80,0.06); margin-top: 13px; border-radius: 8px; }
        .card-error { border-left: 5px solid #f44336; padding: 18px; background: rgba(244,67,54,0.06); margin-top: 13px; border-radius: 8px; }
        .card-hint { border-left: 5px solid #ffb142; padding: 18px; background: rgba(255,177,66,0.06); margin-top: 13px; color: #ffda79; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)


# ==========================================
# GENERADORES VECTORIALES GRÁFICOS (SVG)
# ==========================================

def obtener_svg_atomo(modelo_nombre):
    """
    Genera diagramas vectoriales escalables representativos de la evolución cronológica del átomo.
    Usa elementos nativos HTML5/SVG con alto contraste para asegurar legibilidad en entornos oscuros.
    """
    # Sanitización de datos de entrada
    nombre = str(modelo_nombre)
    
    if "Dalton" in nombre:
        # Esfera maciza, indivisible y sin subpartículas
        return """<svg viewBox='0 0 100 100' width='90' height='90'>
            <circle cx='50' cy='50' r='35' fill='none' stroke='#b0bec5' stroke-width='3'/>
            <circle cx='50' cy='50' r='32' fill='rgba(176, 190, 197, 0.1)'/>
        </svg>"""
        
    elif "Thomson" in nombre:
        # Modelo del 'budín de pasas': masa positiva continua con electrones incrustados
        return """<svg viewBox='0 0 100 100' width='90' height='90'>
            <circle cx='50' cy='50' r='35' fill='#9c27b0' fill-opacity='0.15' stroke='#9c27b0' stroke-width='2'/>
            <text x='50' y='56' fill='#9c27b0' font-size='20' font-weight='bold' text-anchor='middle'>+</text>
            <circle cx='32' cy='40' r='4' fill='#00e5ff'/>
            <circle cx='68' cy='42' r='4' fill='#00e5ff'/>
            <circle cx='50' cy='28' r='4' fill='#00e5ff'/>
            <circle cx='48' cy='72' r='4' fill='#00e5ff'/>
        </svg>"""
        
    elif "Rutherford" in nombre:
        # Núcleo denso positivo central con órbitas elípticas masivas abiertas
        return """<svg viewBox='0 0 100 100' width='90' height='90'>
            <circle cx='50' cy='50' r='5' fill='#e91e63'/>
            <ellipse cx='50' cy='50' rx='38' ry='12' fill='none' stroke='#2196f3' stroke-width='1.2' transform='rotate(30 50 50)'/>
            <ellipse cx='50' cy='50' rx='38' ry='12' fill='none' stroke='#2196f3' stroke-width='1.2' transform='rotate(150 50 50)'/>
            <circle cx='20' cy='33' r='3' fill='#00e5ff'/>
        </svg>"""
        
    elif "Bohr" in nombre:
        # Órbitas circulares concéntricas de energía cuantizada fija
        return """<svg viewBox='0 0 100 100' width='90' height='90'>
            <circle cx='50' cy='50' r='6' fill='#ff9800'/>
            <circle cx='50' cy='50' r='20' fill='none' stroke='#ffb142' stroke-width='1' stroke-dasharray='3 3'/>
            <circle cx='50' cy='50' r='36' fill='none' stroke='#ffb142' stroke-width='1' stroke-dasharray='3 3'/>
            <circle cx='64' cy='36' r='3' fill='#00e5ff'/>
            <circle cx='14' cy='50' r='3' fill='#00e5ff'/>
        </svg>"""
        
    else:
        # Schrödinger: Modelo mecánico cuántico con gradiente de densidad probabilística radial (orbital 3D)
        return """<svg viewBox='0 0 100 100' width='90' height='90'>
            <defs>
                <radialGradient id='cloudGrad' cx='50%' cy='50%' r='50%'>
                    <stop offset='0%' stop-color='#00e5ff' stop-opacity='0.8'/>
                    <stop offset='50%' stop-color='#00e5ff' stop-opacity='0.3'/>
                    <stop offset='100%' stop-color='#00e5ff' stop-opacity='0'/>
                </radialGradient>
            </defs>
            <circle cx='50' cy='50' r='6' fill='#ffffff'/>
            <circle cx='50' cy='50' r='40' fill='url(#cloudGrad)'/>
        </svg>"""


def generar_svg_enlace(sym1, f1, c1, sym2, f2, c2):
    """
    Generates a dynamic chemical bond diagram using scaling parameters.
    Alters the center of the shared cloud ($x$-coordinate) towards the more electronegative atom.
    """
    try:
        val1 = float(f1)
        val2 = float(f2)
    except (ValueError, TypeError):
        val1, val2 = 2.0, 2.0

    # Determinación estequiométrica del centro de densidad de los electrones compartidos
    if val1 > val2:
        ellipse_x = 100
    elif val2 > val1:
        ellipse_x = 140
    else:
        ellipse_x = 120
        
    return f"""<div style='display:flex; justify-content:center; align-items:center; width:100%; height:130px;'>
        <svg viewBox='0 0 240 120' width='100%' height='100%'>
            <!-- Átomo Reactante A -->
            <circle cx='70' cy='60' r='23' fill='{str(c1)}' opacity='0.85' stroke='#ffffff' stroke-width='1'/>
            <text x='70' y='67' fill='#000000' font-weight='bold' font-size='16' text-anchor='middle'>{str(sym1)}</text>
            
            <!-- Átomo Reactante B -->
            <circle cx='170' cy='60' r='19' fill='{str(c2)}' opacity='0.85' stroke='#ffffff' stroke-width='1'/>
            <text x='170' y='66' fill='#000000' font-weight='bold' font-size='14' text-anchor='middle'>{str(sym2)}</text>
            
            <!-- Nube de Interacción o Enlace Compartido -->
            <ellipse cx='{ellipse_x}' cy='60' rx='68' ry='32' fill='none' stroke='#ffffff' stroke-width='1.5' stroke-dasharray='4 4'/>
        </svg>
    </div>"""


# ==========================================
# MOTOR LOGICO DE LOGROS Y APRENDIZAJE
# ==========================================

def mezclar_memorama():
    """
    Construye y baraja de forma aleatoria el tablero inmutable de emparejamiento.
    Retorna una lista estructurada con tuplas de control conceptual.
    """
    contenido = [
        ("Dalton (1810)", 1), ("Materia indivisible sin cargas", 1),
        ("Thomson (1897)", 2), ("Esfera positiva con electrones", 2),
        ("Rutherford (1911)", 3), ("Núcleo denso positivo", 3),
        ("Bohr (1913)", 4), ("Órbitas circulares cuantizadas", 4),
        ("Schrödinger (1926)", 5), ("Orbitales de densidad 3D", 5)
    ]
    random.shuffle(contenido)
    return contenido
