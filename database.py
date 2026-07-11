import streamlit as st
from supabase import create_client, Client

# --- Cargador Inteligente de Secretos ---
def get_secret(key):
    if key in st.secrets: return st.secrets[key]
    elif "supabase" in st.secrets and key in st.secrets["supabase"]: return st.secrets["supabase"][key]
    else: return None

@st.cache_resource
def init_supabase() -> Client:
    url = get_secret("SUPABASE_URL")
    key = get_secret("SUPABASE_KEY")
    return create_client(url, key)

supabase = init_supabase()

# --- PUENTES DE COMPATIBILIDAD (LEGACY) ---
# Estas funciones evitan que app.py falle al buscar código antiguo

def inicializar_db():
    """Puente para app.py: Ya no es necesaria, pero la mantenemos para no romper el flujo."""
    pass

def obtener_password_admin():
    """Restaura la función que app.py requiere para validar el acceso admin."""
    # Busca la contraseña en los secretos, si no existe devuelve un valor seguro para evitar crash
    return st.secrets.get("ADMIN_PASSWORD", "temporal_admin_123")

# --- FUNCIÓN NUEVA Y OPTIMIZADA ---
def guardar_registro_juego(alumno_id: str, dia_modulo: int, puntaje: int, precision_pct: int, metadata_juego: dict) -> bool:
    payload = {
        "alumno_id": alumno_id, "dia_modulo": dia_modulo, "puntaje": puntaje,
        "precision_pct": precision_pct, "metadata_juego": metadata_juego
    }
    try:
        supabase.table("historial_juegos").insert(payload).execute()
        return True
    except Exception as e:
        return False
