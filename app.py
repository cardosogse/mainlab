import streamlit as st
import pandas as pd
import time
import database as db
from typing import Dict, Optional, Any, Final
from assets import cargar_estilos, mezclar_memorama

# Constantes de control
VECES_VIDAS_MAX: Final[int] = 3
ID_MODULO_ACTUAL: Final[str] = "1"

# Configuración inicial
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
db.inicializar_db()

def init_session_state() -> None:
    """Inicializa de forma segura y tipada el estado de la aplicación."""
    defaults: Dict[str, Any] = {
        'auth': None,
        'token_actual': None,
        'procesando': False,
        'ultimo_minuto_sincronizado': -1,
        'puntos_acumulados': 0,
        'vidas': VECES_VIDAS_MAX,
        'tiempo_estudio_min': 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()
pass_maestra_actual: str = db.obtener_password_admin()

def hidratar_sesion_alumno(token: str, datos_db: Dict[str, Any]) -> None:
    """
    Hidrata el estado con validación de existencia de llaves 
    para prevenir KeyError en entornos de producción.
    """
    try:
        st.session_state['token_actual'] = token
        st.session_state['puntos_acumulados'] = datos_db.get("puntos", 0)
        st.session_state['vidas'] = datos_db.get("vidas", VECES_VIDAS_MAX)
        st.session_state['tiempo_historico_min'] = datos_db.get("tiempo", 0)
        st.session_state['tiempo_estudio_min'] = datos_db.get("tiempo", 0)
        st.session_state['inicio_sesion_unix'] = time.time()
        st.session_state['ultimo_minuto_sincronizado'] = 0
        
        if 'memo_tablero' not in st.session_state or not st.session_state['memo_tablero']:
            st.session_state['memo_tablero'] = mezclar_memorama()
        
        st.query_params["token"] = token
    except Exception as e:
        st.error(f"Error crítico en hidratación de sesión: {e}")

# Escudo anti-refresco
if st.session_state['auth'] is None and "token" in st.query_params:
    token_url: str = st.query_params["token"].strip()
    es_valido, payload = db.validar_token(token_url)
    if es_valido and isinstance(payload, dict):
        st.session_state['auth'] = 'usuario'
        hidratar_sesion_alumno(token_url, payload)
        st.rerun()

# Cabecera Global
st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)

# Lógica de Cierre
if st.session_state['auth'] is not None:
    _, col_logout = st.columns([4, 1])
    with col_logout:
        if st.button("Cerrar Sesión 🚪", use_container_width=True, disabled=st.session_state['procesando']):
            st.session_state['procesando'] = True
            if st.session_state['auth'] == 'usuario':
                db.sincronizar_progreso_db(
                    st.session_state['token_actual'], 
                    st.session_state['puntos_acumulados'], 
                    ID_MODULO_ACTUAL, 
                    st.session_state['vidas'], 
                    st.session_state['tiempo_estudio_min']
                )
            st.session_state['auth'] = None
            st.query_params.clear()
            st.session_state['procesando'] = False
            st.rerun()

# [Continuación de vistas de Auth y Admin omitida para brevedad, disponible bajo demanda]
