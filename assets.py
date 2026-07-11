import streamlit as st
import random

def cargar_estilos():
    """
    Inyecta los estilos CSS nativos de alta fidelidad.
    Restaura la estética de laboratorio cibernético nocturno (Dark/Cyber-Lab Mode)
    y hace brillar el sufijo 'Lab' con un efecto de neón cian radiante.
    """
    estilos = """
    <style>
    /* --- CONFIGURACIÓN GLOBAL DEL ENTORNO OSCURO DE LABORATORIO --- */
    [data-testid="stHeader"] { visibility: hidden; }
    footer { visibility: hidden; }
    
    /* Fondo oscuro profundo para simular una pantalla de analizador bioquímico */
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    /* Contenedor principal del encabezado */
    .logo-container {
        text-align: center;
        padding: 20px 0 10px 0;
        margin-bottom: 25px;
    }
    
    /* --- EFECTO DE NEÓN RADIANTE DE MAINLAB --- */
    .main-title {
        font-family: 'Courier New', Courier, monospace, sans-serif;
        font-weight: 800;
        font-size: 3.5rem;
        color: #ffffff;
        margin: 0;
        letter-spacing: 2px;
    }
    
    /* Sufijo Lab resplandeciente en cian bioquímico */
    .main-title-suffix {
        color: #00f2fe;
        text-shadow: 0 0 5px #00f2fe, 
                     0 0 10px #00f2fe, 
                     0 0 20px #00f2fe, 
                     0 0 40px #4facfe;
        animation: pulsar 2.5s infinite alternate;
    }
    
    .main-subtitle {
        font-family: 'Arial', sans-serif;
        font-style: italic;
        font-size: 1.1rem;
        color: #8b949e;
        margin-top: 8px;
    }
    
    @keyframes pulsar {
        0% { text-shadow: 0 0 4px #00f2fe, 0 0 8px #00f2fe, 0 0 15px #00f2fe; }
        100% { text-shadow: 0 0 6px #00f2fe, 0 0 14px #00f2fe, 0 0 25px #00f2fe, 0 0 50px #4facfe; }
    }
    
    /* --- COMPONENTES DE INTERFAZ Y PANELES MÓVILES --- */
    .lab-panel {
        background-color: #161b22;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    
    .login-box {
        max-width: 500px;
        margin: 0 auto;
        background-color: #161b22;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #30363d;
        box-shadow: 0 8px 24px rgba(0,0,0,0.6);
    }
    
    .dashboard-triage {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #00f2fe;
        margin-bottom: 25px;
    }
    
    /* --- DÍA 1: VISUALIZADOR DE ESPECTROMETRÍA --- */
    .particula {
        display: inline-block;
        border-radius: 50%;
        margin: 4px;
        box-shadow: inset -3px -3px 6px rgba(0,0,0,0.6), 0 0 8px rgba(255,255,255,0.1);
        transition: transform 0.2s;
    }
    .particula:hover { transform: scale(1.2); }
    .proton { background: radial-gradient(circle at 35%, #ff6b6b, #cc0000); width: 22px; height: 22px; }
    .neutron { background: radial-gradient(circle at 35%, #9499a7, #4e515a); width: 22px; height: 22px; }
    .electron { background: radial-gradient(circle at 35%, #64d8cb, #00a896); width: 12px; height: 12px; box-shadow: 0 0 6px #00f2fe; }

    /* --- DÍA 2: CÁMARAS DE COLISIÓN QUÍMICA --- */
    .nube-apolar {
        width: 100%; height: 120px;
        border-radius: 60px;
        background: radial-gradient(circle at 50%, #21262d 0%, #161b22 100%);
        border: 2px dashed #30363d;
        display: flex; justify-content: space-around; align-items: center;
        color: #c9d1d9; font-weight: bold; font-size: 1.5rem;
    }
    .nube-polar {
        width: 100%; height: 120px;
        border-radius: 60px 120px 120px 60px;
        background: radial-gradient(circle at 75%, #ff3860 0%, #1f242c 100%);
        border: 2px solid #ff3860;
        display: flex; justify-content: space-around; align-items: center;
        color: white; font-weight: bold; font-size: 1.5rem;
        box-shadow: 0 0 15px rgba(255,56,96,0.3);
    }
    .ruptura-ionica {
        display: flex; justify-content: space-around; width: 100%; padding: 15px 0;
    }
    .ion-cat, .ion-an {
        width: 95px; height: 95px;
        border-radius: 50%;
        display: flex; justify-content: center; align-items: center;
        font-weight: bold; color: white; font-size: 1.3rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.6);
    }
    .ion-cat { background: radial-gradient(circle at 35%, #4facfe, #0052d4); border: 2px solid #00f2fe; box-shadow: 0 0 15px rgba(0,242,254,0.4); }
    .ion-an { background: radial-gradient(circle at 35%, #ff0844, #990022); border: 2px solid #ff0844; box-shadow: 0 0 15px rgba(255,8,68,0.4); }

    /* --- DÍA 6: DINÁMICA DE ERITROCITOS --- */
    .plasma-sanguineo {
        background-color: #1a0f12;
        border: 2px dashed #ff3860;
        border-radius: 16px;
        padding: 30px;
        display: flex; justify-content: center; align-items: center;
        height: 260px; margin-top: 15px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
    }
    .eritrocito-isotonico {
        width: 125px; height: 125px;
        border-radius: 50%;
        background: radial-gradient(circle at 35%, #ff4d4d 20%, #990000 80%);
        box-shadow: 0px 6px 15px rgba(0,0,0,0.6), inset -10px -10px 20px rgba(0,0,0,0.4);
    }
    .eritrocito-hipotonico {
        width: 185px; height: 185px;
        border-radius: 50%;
        background: radial-gradient(circle at 35%, #ff6666 10%, #cc0000 85%);
        box-shadow: 0px 0px 35px rgba(255,77,77,0.7), inset -5px -5px 15px rgba(0,0,0,0.3);
    }
    .eritrocito-hipertonico {
        width: 95px; height: 95px;
        border-radius: 35% 65% 60% 40% / 45% 40% 60% 55%; 
        background: radial-gradient(circle at 35%, #730000 30%, #400000 90%);
        box-shadow: inset 6px 6px 18px rgba(0,0,0,0.8), 0 4px 8px rgba(0,0,0,0.5);
    }
    </style>
    """
    st.markdown(estilos, unsafe_allow_html=True)

def mezclar_memorama():
    """
    Genera y mezcla un tablero base estable para el minijuego de memoria.
    Mantiene la consistencia del estado instruccional del estudiante.
    """
    conceptos = ["Na+", "Catión", "Cl-", "Anión", "H2O", "Dipolo", "Lípido", "Apolar"]
    tablero = conceptos * 2
    random.shuffle(tablero)
    return tablero

