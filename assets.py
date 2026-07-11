import streamlit as st
import random

def cargar_estilos():
    """
    Inyecta los estilos CSS nativos de alta fidelidad del Sistema 1.
    Restaura el fondo del universo con estrellas centelleantes fijas,
    el pulso de neón original y la interactividad reactiva de los botones.
    """
    estilos = """
    <style>
        [data-testid="stHeader"] { visibility: hidden; }
        footer { visibility: hidden; }
        
        /* --- FONDO DEL UNIVERSO ESTRELLADO (SISTEMA 1) --- */
        .stApp {
            background: radial-gradient(circle at center, #0a0e17 0%, #030508 100%) !important;
            background-attachment: fixed !important;
            color: #c9d1d9;
        }
        
        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: 
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 40px);
            background-size: 550px 550px, 350px 350px, 250px 250px;
            background-position: 0 0, 40px 60px, 130px 270px;
            opacity: 0.25;
            z-index: 0;
            pointer-events: none;
        }
        
        .logo-container {
            text-align: center;
            padding: 20px 0 10px 0;
            margin-bottom: 25px;
            position: relative;
            z-index: 1;
        }
        
        .main-title {
            font-family: 'Courier New', Courier, monospace, sans-serif;
            font-weight: 800;
            font-size: 3.5rem;
            color: #ffffff;
            margin: 0;
            letter-spacing: 2px;
        }
        
        .main-title-suffix {
            color: #00f2fe;
            text-shadow: 0 0 5px #00f2fe, 0 0 10px #00f2fe, 0 0 20px #00f2fe, 0 0 40px #4facfe;
            animation: pulso-neon 2.5s infinite alternate ease-in-out;
        }
        
        .main-subtitle {
            font-family: 'Arial', sans-serif;
            font-style: italic;
            font-size: 1.1rem;
            color: #8b949e;
            margin-top: 8px;
        }
        
        @keyframes pulso-neon {
            0% { text-shadow: 0 0 4px #00f2fe, 0 0 8px #00f2fe, 0 0 15px #00f2fe; opacity: 0.85; }
            100% { text-shadow: 0 0 6px #00f2fe, 0 0 14px #00f2fe, 0 0 25px #00f2fe, 0 0 50px #4facfe; opacity: 1; }
        }
        
        .stButton>button {
            background: rgba(0, 242, 254, 0.02) !important;
            color: #00f2fe !important;
            border: 1px solid rgba(0, 242, 254, 0.3) !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: bold !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        
        .stButton>button:hover {
            background: rgba(0, 242, 254, 0.12) !important;
            border-color: #00f2fe !important;
            color: #ffffff !important;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.4) !important;
        }
        
        .lab-panel {
            background-color: rgba(22, 27, 34, 0.7);
            padding: 22px;
            border-radius: 12px;
            border: 1px solid #30363d;
            margin-bottom: 20px;
            backdrop-filter: blur(8px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }
        
        .login-box {
            max-width: 500px;
            margin: 0 auto;
            background-color: rgba(22, 27, 34, 0.8);
            padding: 30px;
            border-radius: 12px;
            border: 1px solid #30363d;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.6);
        }
        
        .dashboard-triage {
            background: linear-gradient(135deg, rgba(22,27,34,0.8) 0%, rgba(13,17,23,0.8) 100%);
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #00f2fe;
            margin-bottom: 25px;
            backdrop-filter: blur(6px);
        }
        
        .particula { display: inline-block; border-radius: 50%; margin: 4px; box-shadow: inset -3px -3px 6px rgba(0,0,0,0.6); }
        .proton { background: radial-gradient(circle at 35%, #ff6b6b, #cc0000); width: 22px; height: 22px; }
        .neutron { background: radial-gradient(circle at 35%, #9499a7, #4e515a); width: 22px; height: 22px; }
        .electron { background: radial-gradient(circle at 35%, #64d8cb, #00a896); width: 12px; height: 12px; box-shadow: 0 0 6px #00f2fe; }
        
        .nube-apolar {
            width: 100%; height: 120px; border-radius: 60px;
            background: radial-gradient(circle at 50%, #21262d 0%, #161b22 100%);
            border: 2px dashed #30363d; display: flex; justify-content: space-around; align-items: center;
        }
        .nube-polar {
            width: 100%; height: 120px; border-radius: 60px 120px 120px 60px;
            background: radial-gradient(circle at 75%, #ff3860 0%, #1f242c 100%);
            border: 2px solid #ff3860; display: flex; justify-content: space-around; align-items: center;
            box-shadow: 0 0 15px rgba(255,56,96,0.3);
        }
        .ruptura-ionica { display: flex; justify-content: space-around; width: 100%; padding: 15px 0; }
        .ion-cat, .ion-an { width: 90px; height: 90px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-weight: bold; color: white; }
        .ion-cat { background: radial-gradient(circle at 35%, #4facfe, #0052d4); border: 2px solid #00f2fe; }
        .ion-an { background: radial-gradient(circle at 35%, #ff0844, #990022); border: 2px solid #ff0844; }
        
        .plasma-sanguineo {
            background-color: #1a0f12; border: 2px dashed #ff3860; border-radius: 16px;
            padding: 30px; display: flex; justify-content: center; align-items: center; height: 240px;
        }
        .eritrocito-isotonico { width: 120px; height: 120px; border-radius: 50%; background: radial-gradient(circle at 35%, #ff4d4d 20%, #990000 80%); }
        .eritrocito-hipotonico { width: 170px; height: 170px; border-radius: 50%; background: radial-gradient(circle at 35%, #ff6666 10%, #cc0000 85%); box-shadow: 0 0 25px rgba(255,77,77,0.6); }
        .eritrocito-hypertonico { width: 90px; height: 90px; border-radius: 35% 65% 60% 40%; background: radial-gradient(circle at 35%, #730000 30%, #400000 90%); }
    </style>
    """
    st.markdown(estilos, unsafe_allow_html=True)

def mezclar_memorama():
    conceptos = ["Na+", "Catión", "Cl-", "Anión", "H2O", "Dipolo", "Lípido", "Apolar"]
    tablero = conceptos * 2
    random.shuffle(tablero)
    return tablero
