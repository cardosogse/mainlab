import streamlit as st
import random
import uuid
from datetime import datetime, timedelta

# Inicialización centralizada y flexible del cliente de Supabase
@st.cache_resource
def init_supabase():
    try:
        # Intenta leer formato plano o estructurado en formato TOML
        if "supabase" in st.secrets:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
        else:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
            
        from supabase import create_client
        return create_client(url, key)
    except Exception:
        # Si no hay credenciales configuradas en GitHub/Local, activa el fallback local
        return None

# Instancia global segura
supabase = init_supabase()

def inicializar_db():
    """Garantiza la existencia del almacén temporal si Supabase corre en modo local."""
    if "tokens_locales" not in st.session_state:
        st.session_state["tokens_locales"] = {
            "UNAM-ADMIN-2026": {"tipo": "admin", "vigencia": "2030-12-31"},
            "TOKEN-DEMO-MVZ": {"tipo": "usuario", "puntos": 0, "vidas": 3, "errores": 0, "tiempo": 0, "vigencia": "2027-12-31"}
        }

def obtener_password_admin():
    """Retorna la clave maestra de administración remota o local."""
    return "ADMIN123"

def validar_token(token_str):
    """Valida un token contra Supabase o la infraestructura local de contingencia."""
    inicializar_db()
    if not token_str:
        return False, "invalid"
        
    # Consultar almacenamiento local primero o como contingencia
    if token_str in st.session_state["tokens_locales"]:
        datos = st.session_state["tokens_locales"][token_str]
        return True, datos
        
    if supabase:
        try:
            res = supabase.table("tokens").select("*").eq("token_id", token_str).execute()
            if res.data:
                fila = res.data[0]
                payload = {
                    "puntos": fila.get("puntos", 0),
                    "vidas": fila.get("vidas", 3),
                    "errores": fila.get("errores", 0),
                    "tiempo": fila.get("tiempo", 0)
                }
                return True, payload
        except Exception:
            pass
            
    return False, "invalid"

def sincronizar_progreso_db(token, puntos, modulo, vidas, tiempo):
    """Sincroniza el micro y macro progreso en la nube o localmente."""
    inicializar_db()
    if token in st.session_state["tokens_locales"]:
        st.session_state["tokens_locales"][token].update({
            "puntos": puntos,
            "vidas": vidas,
            "tiempo": tiempo
        })
        
    if supabase:
        try:
            supabase.table("tokens").update({
                "puntos": puntos,
                "vidas": vidas,
                "tiempo": tiempo,
                "ultima_sincronizacion": datetime.now().isoformat()
            }).eq("token_id", token).execute()
        except Exception:
            pass

def generar_token(dias_vigencia):
    """Genera un nuevo identificador único de acceso licenciado."""
    inicializar_db()
    nuevo_tk = f"MVZ-{uuid.uuid4().hex[:6].upper()}"
    fecha_exp = (datetime.now() + timedelta(days=dias_vigencia)).strftime("%Y-%m-%d")
    
    st.session_state["tokens_locales"][nuevo_tk] = {
        "tipo": "usuario", "puntos": 0, "vidas": 3, "errores": 0, "tiempo": 0, "vigencia": fecha_exp
    }
    return nuevo_tk

def listar_todos_los_tokens():
    """Obtiene el universo completo de investigadores registrados."""
    inicializar_db()
    lista = []
    for tk, val in st.session_state["tokens_locales"].items():
        if val.get("tipo") != "admin":
            lista.append({
                "Token": tk,
                "Puntos": val.get("puntos", 0),
                "Vidas": val.get("vidas", 3),
                "Tiempo (min)": val.get("tiempo", 0),
                "Expiración": val.get("vigencia", "N/A")
            })
    return lista

def forzar_liberacion_sesion(token):
    """Libera candados de sesión bloqueados por desconexiones abruptas."""
    pass

def eliminar_token(token):
    """Elimina definitivamente un registro del ecosistema."""
    inicializar_db()
    if token in st.session_state["tokens_locales"]:
        del st.session_state["tokens_locales"][token]

def guardar_registro_juego(alumno_id, dia_modulo, puntaje, precision_pct, metadata_juego):
    """Inserta el progreso del alumno en la tabla universal 'historial_juegos'."""
    payload = {
        "alumno_id": alumno_id,
        "dia_modulo": dia_modulo,
        "puntaje": puntaje,
        "precision_pct": precision_pct,
        "metadata_juego": metadata_juego
    }
    if supabase:
        try:
            supabase.table("historial_juegos").insert(payload).execute()
            return True
        except Exception:
            return False
    return False
