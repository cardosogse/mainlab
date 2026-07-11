import streamlit as st
from supabase import create_client, Client

# QUITAMOS el @st.cache_resource temporalmente
def init_supabase() -> Client:
    # Depuración: Verificamos si los secretos existen
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Error detectado al leer secretos: {e}")
        st.stop()

# Instancia global
supabase = init_supabase()

def guardar_registro_juego(alumno_id, dia_modulo, puntaje, precision_pct, metadata_juego):
    payload = {
        "alumno_id": alumno_id,
        "dia_modulo": dia_modulo,
        "puntaje": puntaje,
        "precision_pct": precision_pct,
        "metadata_juego": metadata_juego
    }
    try:
        supabase.table("historial_juegos").insert(payload).execute()
        return True
    except Exception:
        return False
