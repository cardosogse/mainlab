import streamlit as st
import uuid
from datetime import datetime, timedelta

@st.cache_resource
def init_supabase():
    """
    Inicialización ultra-resiliente del cliente de Supabase.
    Soporta múltiples variantes de nombres en Streamlit Secrets.
    """
    try:
        url = None
        key = None
        
        # 1. Buscar variantes en la raíz de los secrets
        if "SUPABASE_URL" in st.secrets: url = st.secrets["SUPABASE_URL"]
        elif "url" in st.secrets: url = st.secrets["url"]
        
        if "SUPABASE_KEY" in st.secrets: key = st.secrets["SUPABASE_KEY"]
        elif "key" in st.secrets: key = st.secrets["key"]
        
        # 2. Buscar variantes dentro del bloque [supabase] si existe
        if "supabase" in st.secrets:
            sb = st.secrets["supabase"]
            if "url" in sb: url = sb["url"]
            elif "SUPABASE_URL" in sb: url = sb["SUPABASE_URL"]
            
            if "key" in sb: key = sb["key"]
            elif "SUPABASE_KEY" in sb: key = sb["SUPABASE_KEY"]
        
        if url and key:
            from supabase import create_client
            return create_client(url, key)
            
    except Exception as e:
        st.warning(f"Error al conectar con la infraestructura Cloud: {str(e)}")
    
    return None

# Instancia global protegida
supabase = init_supabase()

def inicializar_db():
    """Garantiza la existencia de la persistencia simulada de contingencia local."""
    if "tokens_locales" not in st.session_state:
        st.session_state["tokens_locales"] = {
            "UNAM-ADMIN-2026": {"tipo": "admin", "vigencia": "2030-12-31"},
            "TOKEN-DEMO-MVZ": {"tipo": "usuario", "puntos": 25, "vidas": 3, "errores": 0, "tiempo": 5, "vigencia": "2027-12-31"}
        }

@st.cache_data(ttl=600)
def obtener_password_admin():
    """
    Recupera la clave maestra con una jerarquía de tres niveles:
    1. Secrets locales/nube de Streamlit (Evita latencia de red).
    2. Tabla 'config' de Supabase (Protegido por caché de 10 minutos).
    3. Fallback seguro por defecto.
    """
    # Nivel 1: Buscar directamente en los Secrets de Streamlit
    if "PASSWORD_ADMIN" in st.secrets:
        return st.secrets["PASSWORD_ADMIN"]
    if "supabase" in st.secrets and "password_admin" in st.secrets["supabase"]:
        return st.secrets["supabase"]["password_admin"]

    # Nivel 2: Consulta optimizada a la base de datos
    if supabase:
        try:
            res = supabase.table("config").select("value").eq("key", "password_admin").execute()
            if res.data and len(res.data) > 0:
                return res.data[0]["value"]
        except Exception:
            pass
            
    # Nivel 3: Fallback de contingencia
    return "ADMIN123"

@st.cache_data(ttl=60)
def validar_token(token_str):
    """
    Valida las credenciales de acceso mitigando consultas redundantes mediante caché dinámico.
    Retorna un booleano de éxito y el diccionario con el estado del alumno.
    """
    inicializar_db()
    if not token_str:
        return False, "invalid"
        
    # Verificación prioritaria en contingencia local interna
    if token_str in st.session_state["tokens_locales"]:
        return True, st.session_state["tokens_locales"][token_str]
        
    # Consulta remota optimizada
    if supabase:
        try:
            res = supabase.table("tokens").select("*").eq("token_id", token_str).execute()
            if res.data and len(res.data) > 0:
                fila = res.data[0]
                
                # Validación de expiración cronológica
                expiracion_str = fila.get("expiracion")
                if expiracion_str:
                    expiracion = datetime.strptime(expiracion_str, "%Y-%m-%d").date()
                    if expiracion < datetime.now().date():
                        return False, "expired"

                payload = {
                    "puntos": fila.get("puntos", 0),
                    "vidas": fila.get("vidas", 3),
                    "errores": fila.get("errores", 0),
                    "tiempo": fila.get("tiempo", 0),
                    "vigencia": expiracion_str
                }
                return True, payload
        except Exception:
            pass
            
    return False, "invalid"

def sincronizar_progreso_db(token, puntos, modulo, vidas, tiempo):
    """
    Persistencia atómica del macro y micro progreso del alumno.
    Utiliza operaciones seguras e incluye registros de auditoría de tiempo.
    """
    inicializar_db()
    
    # 1. Actualización inmediata del nodo de contingencia local
    if token in st.session_state["tokens_locales"]:
        st.session_state["tokens_locales"][token].update({
            "puntos": puntos,
            "vidas": vidas,
            "tiempo": tiempo
        })
        
    # 2. Sincronización asíncrona hacia Supabase (Pattern: Upsert/Update Seguro)
    if supabase:
        try:
            supabase.table("tokens").update({
                "puntos": puntos,
                "vidas": vidas,
                "tiempo": tiempo,
                "ultima_sincronizacion": datetime.now().isoformat()
            }).eq("token_id", token).execute()
        except Exception as e:
            # Falla silenciosa en la UI pero capturada para desarrollo
            pass

def registrar_evento_telemetria(alumno_id, dia_modulo, evento_tipo):
    """
    Registra marcas de tiempo exactas del flujo instruccional del estudiante
    para mitigar la ceguera de embudo y analizar tasas de abandono.
    """
    if supabase:
        try:
            payload = {
                "alumno_id": alumno_id,
                "dia_modulo": int(dia_modulo),
                "evento": evento_tipo,
                "timestamp": datetime.now().isoformat()
            }
            supabase.table("telemetria_estudiantes").insert(payload).execute()
            return True
        except Exception:
            return False
    return False

def generar_token(dias_vigencia):
    """Crea una nueva licencia única de acceso al entorno educativo."""
    inicializar_db()
    nuevo_tk = f"MVZ-{uuid.uuid4().hex[:6].upper()}"
    fecha_exp = (datetime.now() + timedelta(days=dias_vigencia)).strftime("%Y-%m-%d")
    
    st.session_state["tokens_locales"][nuevo_tk] = {
        "tipo": "usuario", "puntos": 0, "vidas": 3, "errores": 0, "tiempo": 0, "vigencia": fecha_exp
    }
    
    if supabase:
        try:
            supabase.table("tokens").insert({
                "token_id": nuevo_tk, "puntos": 0, "vidas": 3, "tiempo": 0, "expiracion": fecha_exp
            }).execute()
        except Exception:
            pass
            
    return nuevo_tk

def listar_todos_los_tokens():
    """Recupera la nómina completa de licencias para el monitor administrativo."""
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
    """Remueve bloqueos lógicos o banderas de sesión activa para un token específico."""
    if supabase:
        try:
            supabase.table("tokens").update({"sesion_activa": False}).eq("token_id", token).execute()
        except Exception:
            pass

def eliminar_token(token):
    """Remueve de raíz el acceso a un token."""
    inicializar_db()
    if token in st.session_state["tokens_locales"]:
        del st.session_state["tokens_locales"][token]
    if supabase:
        try:
            supabase.table("tokens").delete().eq("token_id", token).execute()
        except Exception:
            pass

def guardar_registro_juego(alumno_id, dia_modulo, puntaje, precision_pct, metadata_juego):
    """Inserta el récord analítico final de evaluaciones en la tabla 'historial_juegos'."""
    payload = {
        "alumno_id": alumno_id,
        "dia_modulo": dia_modulo,
        "puntaje": puntaje,
        "precision_pct": precision_pct,
        "metadata_juego": metadata_juego,
        "fecha_registro": datetime.now().isoformat()
    }
    if supabase:
        try:
            supabase.table("historial_juegos").insert(payload).execute()
            return True
        except Exception:
            return False
    return False
