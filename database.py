import streamlit as st
import uuid
from datetime import datetime, timedelta

@st.cache_resource
def init_supabase():
    """Inicialización centralizada y flexible del cliente de Supabase."""
    try:
        if "supabase" in st.secrets:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
        else:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
            
        from supabase import create_client
        return create_client(url, key)
    except Exception as e:
        st.error(f"⚠️ Error crítico en la carga de st.secrets: {str(e)}")
        return None

supabase = init_supabase()

def inicializar_db():
    """Garantiza la existencia del almacén temporal local de contingencia."""
    if "tokens_locales" not in st.session_state:
        st.session_state["tokens_locales"] = {
            "UNAM-ADMIN-2026": {"tipo": "admin", "vigencia": "2030-12-31"},
            "TOKEN-DEMO-MVZ": {"tipo": "usuario", "puntos": 25, "vidas": 3, "errores": 0, "tiempo": 5, "vigencia": "2027-12-31"}
        }

def obtener_password_admin():
    """
    Escáner adaptativo multitabla para Supabase.
    Si la consulta falla, muestra visualmente el error estructural en la interfaz.
    """
    if supabase:
        errores_tablas = []
        
        # Intento 1: Tabla 'config' (Esquema Clave-Valor)
        try:
            res = supabase.table("config").select("value").eq("key", "password_admin").execute()
            if res.data and len(res.data) > 0:
                return res.data[0]["value"]
        except Exception as e:
            errores_tablas.append(f"Tabla 'config' -> {str(e)}")
            
        # Intento 2: Tabla 'admin' (Esquema Directo)
        try:
            res = supabase.table("admin").select("password").execute()
            if res.data and len(res.data) > 0:
                return res.data[0]["password"]
        except Exception as e:
            errores_tablas.append(f"Tabla 'admin' -> {str(e)}")
            
        # Intento 3: Tabla 'usuarios' (Esquema por Roles)
        try:
            res = supabase.table("usuarios").select("password").eq("rol", "admin").execute()
            if res.data and len(res.data) > 0:
                return res.data[0]["password"]
        except Exception as e:
            errores_tablas.append(f"Tabla 'usuarios' -> {str(e)}")

        # Renderizado de diagnóstico en pantalla si la base de datos respondió pero fallaron las tablas
        if errores_tablas:
            with st.sidebar.expander("🔍 DIAGNÓSTICO DE CONEXIÓN SUPABASE", expanded=True):
                st.error("No se localizó la clave maestra en tus tablas actuales:")
                for err in errores_tablas:
                    st.caption(err)
                st.info("Usa la clave temporal de rescate: ADMIN123")

    return "ADMIN123"

def validar_token(token_str):
    """Valida los tokens de acceso contra Supabase o el almacenamiento local."""
    inicializar_db()
    if not token_str:
        return False, "invalid"
        
    if token_str in st.session_state["tokens_locales"]:
        return True, st.session_state["tokens_locales"][token_str]
        
    if supabase:
        try:
            res = supabase.table("tokens").select("*").eq("token_id", token_str).execute()
            if res.data and len(res.data) > 0:
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
    """Sincroniza los avances del estudiante en la nube o localmente."""
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
    """Crea una nueva licencia de acceso y la registra en el sistema."""
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
    """Inserta el récord analítico final en la tabla 'historial_juegos'."""
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
