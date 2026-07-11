import streamlit as st
import random

def cargar_estilos():
    """Inyecta los estilos CSS nativos exactos del diseño original del laboratorio."""
    estilos = """
    <style>
    /* --- INTEGRACIÓN UX SIN BLOQUEO --- */
    [data-testid="stHeader"] { visibility: hidden; }
    footer { visibility: hidden; }
    
    .main-title {
        text-align: center;
        font-family: 'Arial', sans-serif;
        color: #1E3A8A;
        margin-top: -30px;
        margin-bottom: 20px;
    }
    .main-title-suffix {
        color: #3B82F6;
    }
    
    .lab-panel {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 15px;
    }
    
    /* --- DÍA 1: ESPECTRÓMETRO DE MASAS --- */
    .particula {
        display: inline-block;
        border-radius: 50%;
        margin: 3px;
        box-shadow: inset -2px -2px 4px rgba(0,0,0,0.4);
    }
    .proton { background-color: #ff4b4b; width: 20px; height: 20px; }
    .neutron { background-color: #808495; width: 20px; height: 20px; }
    .electron { background-color: #4facfe; width: 10px; height: 10px; }

    /* --- DÍA 2: REACTOR DE FUSIÓN --- */
    .nube-apolar {
        width: 100%; height: 120px;
        border-radius: 60px;
        background: radial-gradient(circle at 50%, #4facfe 0%, #00f2fe 100%);
        display: flex; justify-content: space-around; align-items: center;
        color: white; font-weight: bold; font-size: 1.5rem;
    }
    .nube-polar {
        width: 100%; height: 120px;
        border-radius: 60px 120px 120px 60px;
        background: radial-gradient(circle at 75%, #ff0844 0%, #ffb199 100%);
        display: flex; justify-content: space-around; align-items: center;
        color: white; font-weight: bold; font-size: 1.5rem;
    }
    .ruptura-ionica {
        display: flex; justify-content: space-around; width: 100%;
    }
    .ion-cat, .ion-an {
        width: 90px; height: 90px;
        border-radius: 50%;
        display: flex; justify-content: center; align-items: center;
        font-weight: bold; color: white; font-size: 1.2rem;
        box-shadow: 0 6px 15px rgba(0,0,0,0.2);
    }
    .ion-cat { background: #4facfe; }
    .ion-an { background: #ff0844; }

    /* --- DÍA 6: FLUIDOTERAPIA CLÍNICA --- */
    .plasma-sanguineo {
        background-color: #fce8e8;
        border: 2px dashed #f8b4b4;
        border-radius: 15px;
        padding: 30px;
        display: flex; justify-content: center; align-items: center;
        height: 250px; margin-top: 15px;
    }
    .eritrocito-isotonico {
        width: 120px; height: 120px;
        border-radius: 50%;
        background: radial-gradient(circle at center, #ff7b7b 30%, #cc0000 80%);
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .eritrocito-hipotonico {
        width: 180px; height: 180px;
        border-radius: 50%;
        background: radial-gradient(circle at center, #ff9b9b 10%, #e60000 90%);
        box-shadow: 0px 0px 30px rgba(255,0,0,0.6);
    }
    .eritrocito-hipertonico {
        width: 90px; height: 90px;
        border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%; 
        background: radial-gradient(circle at center, #990000 40%, #660000 90%);
        box-shadow: inset 8px 8px 20px rgba(0,0,0,0.7);
    }
    </style>
    """
    st.markdown(estilos, unsafe_allow_html=True)

def mezclar_memorama():
    """Genera y mezcla un tablero base estable para el minijuego de memoria."""
    conceptos = ["Na+", "Catión", "Cl-", "Anión", "H2O", "Dipolo", "Lípido", "Apolar"]
    tablero = conceptos * 2
    random.shuffle(tablero)
    return tablero
