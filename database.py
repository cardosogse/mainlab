import streamlit as st
from supabase import create_client, Client

# --- Cargador Inteligente de Secretos ---
def get_secret(key):
    """
    Busca la llave en la raíz o en la sección [supabase] para evitar errores de despliegue.
    """
    # Opción 1: Llave en la raíz (formato estándar Streamlit Cloud)
    if key in st.secrets:
        return st.secrets[key]
    # Opción 2: Llave dentro de la sección [supabase] (formato .toml local)
    elif "supabase" in st.secrets and key in st.secrets["supabase"]:
        return st.secrets["supabase"][key]
    else:
        st.error(f"Error: No se encontró la llave '{key}'. Verifica tus secretos en el panel de Streamlit Cloud.")
        st.stop()

@st.cache_resource
def init_supabase() -> Client:
    # Utilizamos el cargador inteligente
    url = get_secret("SUPABASE_URL")
    key = get_secret("SUPABASE_KEY")
    return create_client(url, key)

# Instancia global
supabase = init_supabase()

def guardar_registro_juego(alumno_id: str, dia_modulo: int, puntaje: int, precision_pct: int, metadata_juego: dict) -> bool:
    """
    Inserta el progreso del alumno en la tabla 'historial_juegos'.
    Uso de Failsafe para proteger la experiencia del alumno.
    """
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
    except Exception as e:
        # Silenciamos el error para no romper la app del alumno, 
        # pero mantenemos la lógica de persistencia
        return False
