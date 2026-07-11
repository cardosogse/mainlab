import streamlit as st
from supabase import create_client, Client
from typing import Dict, Any, Final

TABLE_HISTORIAL: Final[str] = "historial_juegos"

@st.cache_resource
def get_supabase_client() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

def guardar_registro_juego(alumno_id: str, dia_modulo: int, puntaje: int, precision: int, meta: Dict[str, Any]) -> bool:
    if not alumno_id or not isinstance(dia_modulo, int):
        return False
    
    try:
        payload = {
            "alumno_id": alumno_id, "dia_modulo": dia_modulo, 
            "puntaje": puntaje, "precision_pct": precision, "metadata_juego": meta
        }
        get_supabase_client().table(TABLE_HISTORIAL).insert(payload).execute()
        return True
    except Exception:
        return False
