import streamlit as st
import time
import database as db
from typing import Dict, Any, Final

VECES_VIDAS_MAX: Final[int] = 3
ID_MODULO_ACTUAL: Final[str] = "1"

def init_session_state() -> None:
    defaults: Dict[str, Any] = {
        'auth': None, 'token_actual': None, 'procesando': False,
        'puntos_acumulados': 0, 'vidas': VECES_VIDAS_MAX
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

def hidratar_sesion_alumno(token: str, datos_db: Dict[str, Any]) -> None:
    st.session_state.update({
        'token_actual': token,
        'puntos_acumulados': datos_db.get("puntos", 0),
        'vidas': datos_db.get("vidas", VECES_VIDAS_MAX),
        'inicio_sesion_unix': time.time()
    })
    st.query_params["token"] = token
