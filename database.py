import sqlite3
import datetime
from datetime import timedelta
import random
import string
import streamlit as st
from supabase import create_client

# ==========================================
# CONFIGURACIÓN Y CLIENTES DE BD
# ==========================================

# Limpieza estricta de espacios en blanco invisibles desde los secretos
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"].strip()
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"].strip()
DB_NAME = st.secrets["config"]["DB_NAME"].strip()
ADMIN_PASSWORD = st.secrets["config"]["ADMIN_PASSWORD"].strip()

# Inicialización segura del cliente de Supabase
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error crítico al conectar con el servidor remoto (Supabase): {e}")
    supabase = None

# ==========================================
# FUNCIONES NATIVAS DE BASE DE DATOS
# ==========================================

def inicializar_db():
    """Crea las tablas locales si no existen y configura la contraseña de administrador."""
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            c = conn.cursor()
            # Tabla de control de accesos y progreso del alumno
            c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso (
                token TEXT PRIMARY KEY, 
                en_uso INTEGER, 
                fecha_expiracion TEXT, 
                score_puntos INTEGER, 
                vidas INTEGER, 
                modulo_actual TEXT,
                intentos_quiz INTEGER, 
                tiempo_estudio_min INTEGER, 
                errores_quiz INTEGER)''')
            
            # Tabla de configuración interna del administrador
            c.execute('''CREATE TABLE IF NOT EXISTS admin_config (key TEXT PRIMARY KEY, value TEXT)''')
            c.execute("INSERT OR IGNORE INTO admin_config VALUES ('password', ?)", (ADMIN_PASSWORD,))
    except sqlite3.Error as e:
        st.error(f"Error al inicializar la base de datos local: {e}")
    finally:
        conn.close()


def generar_token(dias):
    """Genera un token único y lo registra en la base de datos local y remota."""
    prefix = "MLP-" if dias >= 90 else "ML-"
    caracteres_aleatorios = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    token = f"{prefix}{caracteres_aleatorios}"
    fecha_exp = (datetime.date.today() + timedelta(days=dias)).strftime("%Y-%m-%d")
    
    # Registro en SQLite local
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            c = conn.cursor()
            c.execute("INSERT INTO tokens_acceso VALUES (?, 0, ?, 0, 3, '1', 0, 0, 0)", (token, fecha_exp))
    except sqlite3.Error as e:
        st.error(f"Error al guardar el token localmente: {e}")
        return None
    finally:
        conn.close()
    
    # Sincronización remota en Supabase
    if supabase:
        try:
            supabase.table("tokens_acceso").insert({
                "token": token, 
                "en_uso": 0, 
                "fecha_expiracion": fecha_exp,
                "score_puntos": 0, 
                "vidas": 3, 
                "modulo_actual": "1",
                "intentos_quiz": 0, 
                "tiempo_estudio_min": 0, 
                "errores_quizz": 0  # Se mantiene la nomenclatura exacta de tu esquema remoto
            }).execute()
        except Exception:
            pass  # Falla silenciosa para evitar romper la experiencia de usuario si no hay internet
            
    # Al modificar los datos de los tokens, limpiamos el caché de lectura del administrador
    st.cache_data.clear()
    return token


def validar_token(token):
    """Valida el token, controla su expiración y gestiona el estado de uso."""
    conn = sqlite3.connect(DB_NAME)
    res = None
    try:
        with conn:
            c = conn.cursor()
            c.execute("""SELECT score_puntos, vidas, modulo_actual, errores_quiz, tiempo_estudio_min, fecha_expiracion 
                         FROM tokens_acceso WHERE token = ?""", (token,))
            res = c.fetchone()
    except sqlite3.Error as e:
        st.error(f"Error de lectura en validación local: {e}")
        return False, "invalid"
    finally:
        conn.close()

    if res:
        score, vidas, modulo, errores, tiempo_min, fecha_exp = res
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        
        # Control de expiración del token
        if hoy > fecha_exp:
            conn = sqlite3.connect(DB_NAME)
            try:
                with conn:
                    c = conn.cursor()
                    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
            except sqlite3.Error:
                pass
            finally:
                conn.close()
                
            if supabase:
                try:
                    supabase.table("tokens_acceso").update({"en_uso": 0, "modulo_actual": "EXPIRADO"}).eq("token", token).execute()
                except Exception:
                    pass
            return False, "expired"
        
        # Activación del token en uso
        conn = sqlite3.connect(DB_NAME)
        try:
            with conn:
                c = conn.cursor()
                c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token,))
        except sqlite3.Error:
            pass
        finally:
            conn.close()
            
        if supabase:
            try:
                supabase.table("tokens_acceso").update({"en_uso": 1}).eq("token", token).execute()
            except Exception:
                pass
        
        return True, {"puntos": score, "vidas": vidas, "modulo": modulo, "errores": errores, "tiempo": tiempo_min}
        
    return False, "invalid"


def eliminar_token(token):
    """Elimina el registro de un token en ambos entornos de datos."""
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            c = conn.cursor()
            c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token,))
    except sqlite3.Error as e:
        st.error(f"Error al eliminar el token local: {e}")
    finally:
        conn.close()
        
    if supabase:
        try:
            supabase.table("tokens_acceso").delete().eq("token", token).execute()
        except Exception:
            pass
            
    st.cache_data.clear()


def sincronizar_progreso_db(token, puntos, mod, vidas, tiempo_min):
    """Sincroniza de forma segura el progreso del estudiante usando estructuras síncronas."""
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            c = conn.cursor()
            c.execute("""UPDATE tokens_acceso 
                         SET score_puntos = ?, modulo_actual = ?, vidas = ?, tiempo_estudio_min = ? 
                         WHERE token = ?""", (int(puntos), str(mod), int(vidas), int(tiempo_min), token))
    except sqlite3.Error as e:
        st.error(f"Error al sincronizar progreso local: {e}")
    finally:
        conn.close()
        
    if supabase:
        try:
            # Implementación equivalente a un Upsert seguro por llave primaria (token)
            supabase.table("tokens_acceso").update({
                "score_puntos": int(puntos), 
                "modulo_actual": str(mod), 
                "vidas": int(vidas), 
                "tiempo_estudio_min": int(tiempo_min)
            }).eq("token", token).execute()
        except Exception:
            pass
            
    st.cache_data.clear()


def registrar_intento_quiz(token, nuevos_errores, nuevas_vidas, tiempo_min):
    """Incrementa las estadísticas de evaluaciones controlando la integridad referencial."""
    conn = sqlite3.connect(DB_NAME)
    intentos_totales, errores_totales = 0, 0
    try:
        with conn:
            c = conn.cursor()
            c.execute("""UPDATE tokens_acceso 
                         SET intentos_quiz = intentos_quiz + 1, errores_quiz = errores_quiz + ?, 
                             vidas = ?, tiempo_estudio_min = ? 
                         WHERE token = ?""", (int(nuevos_errores), int(nuevas_vidas), int(tiempo_min), token))
            
            c.execute("SELECT intentos_quiz, errores_quiz FROM tokens_acceso WHERE token = ?", (token,))
            res = c.fetchone()
            if res:
                intentos_totales, errores_totales = res
    except sqlite3.Error as e:
        st.error(f"Error al registrar intento de evaluación: {e}")
    finally:
        conn.close()
        
    if supabase and intentos_totales > 0:
        try:
            supabase.table("tokens_acceso").update({
                "vidas": int(nuevas_vidas), 
                "errores_quizz": int(errores_totales), 
                "intentos_quiz": int(intentos_totales), 
                "tiempo_estudio_min": int(tiempo_min)
            }).eq("token", token).execute()
        except Exception:
            pass
            
    st.cache_data.clear()


def otorgar_tiempo_extra_db(token, dias_adicionales=7):
    """Añade días de acceso extendido a un alumno válido."""
    conn = sqlite3.connect(DB_NAME)
    str_fecha = None
    try:
        with conn:
            c = conn.cursor()
            c.execute("SELECT fecha_expiracion FROM tokens_acceso WHERE token = ?", (token,))
            res = c.fetchone()
            if res:
                nueva_fecha = datetime.datetime.strptime(res[0], "%Y-%m-%d").date() + timedelta(days=dias_adicionales)
                str_fecha = nueva_fecha.strftime("%Y-%m-%d")
                c.execute("UPDATE tokens_acceso SET fecha_expiracion = ? WHERE token = ?", (str_fecha, token))
    except sqlite3.Error as e:
        st.error(f"Error al extender vigencia local: {e}")
    finally:
        conn.close()
        
    if supabase and str_fecha:
        try:
            supabase.table("tokens_acceso").update({"fecha_expiracion": str_fecha}).eq("token", token).execute()
        except Exception:
            pass
            
    st.cache_data.clear()


def obtener_password_admin():
    """Recupera la clave maestra de acceso de administración de forma local."""
    conn = sqlite3.connect(DB_NAME)
    res = None
    try:
        with conn:
            c = conn.cursor()
            c.execute("SELECT value FROM admin_config WHERE key = 'password'")
            res = c.fetchone()
    except sqlite3.Error:
        pass
    finally:
        conn.close()
    return res[0] if res else "admin"


@st.cache_data(ttl=600)
def listar_todos_los_tokens():
    """
    Lee de forma optimizada la lista completa de tokens para el panel de administración.
    Utiliza caché de Streamlit por 10 minutos o hasta que ocurra una mutación de datos.
    """
    conn = sqlite3.connect(DB_NAME)
    filas = []
    try:
        with conn:
            c = conn.cursor()
            c.execute("""SELECT token, en_uso, fecha_expiracion, score_puntos, vidas, 
                                modulo_actual, intentos_quiz, tiempo_estudio_min, errores_quiz 
                         FROM tokens_acceso""")
            filas = c.fetchall()
    except sqlite3.Error as e:
        st.error(f"Error al listar credenciales en panel: {e}")
    finally:
        conn.close()
        
    claves = ["Token", "Activo", "Expiracion", "Puntos", "Vidas", "Modulo", "Intentos Quiz", "Tiempo Estudio (min)", "Errores Quiz"]
    return [dict(zip(claves, f)) for f in filas]


def forzar_liberacion_sesion(token):
    """Libera el estado 'en_uso' de un token bloqueado para permitir inicios de sesión nuevos."""
    conn = sqlite3.connect(DB_NAME)
    try:
        with conn:
            c = conn.cursor()
            c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    except sqlite3.Error as e:
        st.error(f"Error al liberar sesión local: {e}")
    finally:
        conn.close()
        
    if supabase:
        try:
            supabase.table("tokens_acceso").update({"en_uso": 0}).eq("token", token).execute()
        except Exception:
            pass
            
    st.cache_data.clear()
