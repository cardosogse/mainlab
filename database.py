import streamlit as st
from supabase import create_client, Client

# Inicialización centralizada y en caché del cliente de Supabase
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

# Instancia global para ser importada en los demás módulos
supabase = init_supabase()

def guardar_registro_juego(alumno_id: str, dia_modulo: int, puntaje: int, precision_pct: int, metadata_juego: dict) -> bool:
    """
    Inserta el progreso del alumno en la tabla universal 'historial_juegos'.
    Utiliza un bloque Failsafe (try-except) para evitar que la app colapse 
    en el celular del alumno si la base de datos no está lista o hay latencia.
    """
    payload = {
        "alumno_id": alumno_id,
        "dia_modulo": dia_modulo,
        "puntaje": puntaje,
        "precision_pct": precision_pct,
        "metadata_juego": metadata_juego  # Supabase absorbe este diccionario como JSONB nativo
    }
    
    try:
        # Intento de inserción en la nube
        supabase.table("historial_juegos").insert(payload).execute()
        return True
    except Exception as e:
        # Falla silenciosa protectora. 
        # (Opcional: puedes dejar el print para depurar en tu consola local)
        # print(f"Error silencioso BD: {e}")
        return False
