import sqlite3
import datetime
from datetime import timedelta
import random
import string
import requests
import streamlit as st

def obtener_llave_secreta(seccion, llave):
    if seccion in st.secrets and llave in st.secrets[seccion]:
        return st.secrets[seccion][llave].strip()
    elif llave in st.secrets:
        return st.secrets[llave].strip()
    return ""

SUPABASE_URL = obtener_llave_secreta("supabase", "SUPABASE_URL")
SUPABASE_KEY = obtener_llave_secreta("supabase", "SUPABASE_KEY")
DB_NAME = "mainlab_v3.db"

# --- CAPA DE CONEXIÓN REST CON LA NUBE (SUPABASE) ---
def _supabase_rest_post(tabla: str, payload: dict):
    if not SUPABASE_URL or not SUPABASE_KEY: return
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{tabla}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        res = requests.post(url, headers=headers, json=payload, timeout=6)
        if res.status_code not in [200, 201]:
            st.error(f"🚨 Error en Supabase (POST {tabla}): Código {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"🚨 Fallo de conexión de red con la nube (POST): {str(e)}")

def _supabase_rest_patch(tabla: str, payload: dict, columna_filtro: str, valor_filtro: str):
    if not SUPABASE_URL or not SUPABASE_KEY: return
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{tabla}?{columna_filtro}=eq.{valor_filtro}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        res = requests.patch(url, headers=headers, json=payload, timeout=6)
        if res.status_code not in [200, 204]:
            st.error(f"🚨 Error en Supabase (PATCH {tabla}): Código {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"🚨 Fallo de conexión de red con la nube (PATCH): {str(e)}")

def _supabase_rest_delete(tabla: str, columna_filtro: str, valor_filtro: str):
    if not SUPABASE_URL or not SUPABASE_KEY: return
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{tabla}?{columna_filtro}=eq.{valor_filtro}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Prefer": "return=minimal"
        }
        res = requests.delete(url, headers=headers, timeout=6)
        if res.status_code not in [200, 204]:
            st.error(f"🚨 Error en Supabase (DELETE {tabla}): Código {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"🚨 Fallo de conexión de red con la nube (DELETE): {str(e)}")

def _supabase_rest_get_singular(tabla: str, columna_filtro: str, valor_filtro: str):
    if not SUPABASE_URL or not SUPABASE_KEY: return None
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{tabla}?{columna_filtro}=eq.{valor_filtro}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        respuesta = requests.get(url, headers=headers, timeout=6)
        if respuesta.status_code == 200:
            registros = respuesta.json()
            return registros[0] if registros else None
        else:
            st.error(f"🚨 Error en Supabase (GET {tabla}): Código {respuesta.status_code} - {respuesta.text}")
    except Exception as e:
        st.error(f"🚨 Fallo de conexión de red con la nube (GET): {str(e)}")
    return None

def _supabase_rest_get_todo(tabla: str):
    if not SUPABASE_URL or not SUPABASE_KEY: return []
    try:
        url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/{tabla}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        respuesta = requests.get(url, headers=headers, timeout=6)
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            st.error(f"🚨 Error en Supabase (GET ALL {tabla}): Código {respuesta.status_code} - {respuesta.text}")
    except Exception as e:
        st.error(f"🚨 Fallo de conexión de red con la nube (GET ALL): {str(e)}")
    return []

# --- CONTROLADORES LOCALES (SQLITE3) ---
def _ejecutar_sql_lectura(query: str, params: tuple = ()):
    try:
        with sqlite3.connect(DB_NAME, timeout=10) as conn:
            c = conn.cursor()
            c.execute(query, params)
            return c.fetchall()
    except sqlite3.Error as e:
        st.error(f"Error de lectura local: {e}")
        return []

def _ejecutar_sql_escritura(query: str, params: tuple = ()):
    try:
        with sqlite3.connect(DB_NAME, timeout=10) as conn:
            c = conn.cursor()
            c.execute(query, params)
            conn.commit()
            return True
    except sqlite3.Error as e:
        st.error(f"Error de escritura local: {e}")
        return False

def inicializar_db():
    try:
        with sqlite3.connect(DB_NAME, timeout=10) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso (
                token TEXT PRIMARY KEY, en_uso INTEGER, fecha_expiracion TEXT, 
                score_puntos INTEGER, vidas INTEGER, modulo_actual TEXT,
                intentos_quiz INTEGER, tiempo_estudio_min INTEGER, errores_quiz INTEGER)''')
            conn.commit()
    except sqlite3.Error as e:
        st.error(f"Fallo al inicializar base de datos local: {e}")

def obtener_password_admin():
    return obtener_llave_secreta("config", "ADMIN_PASSWORD") or "ADMIN123"

def validar_token(token: str):
    query = "SELECT score_puntos, vidas, modulo_actual, errores_quiz, tiempo_estudio_min, fecha_expiracion FROM tokens_acceso WHERE token = ?"
    res = _ejecutar_sql_lectura(query, (token,))
    
    if res:
        score, vidas, modulo, errores, tiempo_min, fecha_exp = res[0]
        if datetime.date.today().strftime("%Y-%m-%d") > fecha_exp:
            return False, "expired"
        return True, {"puntos": score, "vidas": vidas, "modulo": modulo, "errores": errores, "tiempo": tiempo_min}
    
    registro_nube = _supabase_rest_get_singular("tokens_acceso", "token", token)
    if registro_nube:
        fecha_exp = registro_nube.get("fecha_expiracion")
        if datetime.date.today().strftime("%Y-%m-%d") > fecha_exp:
            return False, "expired"
        
        query_insert = """
            INSERT INTO tokens_acceso 
            (token, en_uso, fecha_expiracion, score_puntos, vidas, modulo_actual, intentos_quiz, tiempo_estudio_min, errores_quiz) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        # HOMOLOGACIÓN TRADUCTORA: Convierte 'errores_quizz' de Supabase a 'errores_quiz' local
        _ejecutar_sql_escritura(query_insert, (
            token,
            registro_nube.get("en_uso", 0),
            fecha_exp,
            registro_nube.get("score_puntos", 0),
            registro_nube.get("vidas", 3),
            str(registro_nube.get("modulo_actual", "1")),
            registro_nube.get("intentos_quiz", 0),
            registro_nube.get("tiempo_estudio_min", 0),
            registro_nube.get("errores_quizz", 0)
        ))
        
        return True, {
            "puntos": registro_nube.get("score_puntos", 0),
            "vidas": registro_nube.get("vidas", 3),
            "modulo": str(registro_nube.get("modulo_actual", "1")),
            "errores": registro_nube.get("errores_quizz", 0),
            "tiempo": registro_nube.get("tiempo_estudio_min", 0)
        }
        
    return False, "invalid"

def sincronizar_progreso_db(token: str, puntos: int, mod: str, vidas: int, tiempo_min: int):
    query = "UPDATE tokens_acceso SET score_puntos = ?, modulo_actual = ?, vidas = ?, tiempo_estudio_min = ? WHERE token = ?"
    exito = _ejecutar_sql_escritura(query, (int(puntos), str(mod), int(vidas), int(tiempo_min), token))
    if exito:
        payload_update = {
            "score_puntos": int(puntos), 
            "modulo_actual": str(mod), 
            "vidas": int(vidas), 
            "tiempo_estudio_min": int(tiempo_min)
        }
        _supabase_rest_patch("tokens_acceso", payload_update, "token", token)

def guardar_registro_juego(alumno_id: str, dia_modulo: int, puntaje: int, precision_pct: int, metadata_juego: dict):
    payload = {
        "alumno_id": alumno_id, "dia_modulo": int(dia_modulo), "puntaje": int(puntaje),
        "precision_pct": int(precision_pct), "metadata_juego": metadata_juego
    }
    _supabase_rest_post("historial_juegos", payload)
    return True

def generar_token(dias: int) -> str:
    token = f"ML-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
    fecha_exp = (datetime.date.today() + timedelta(days=dias)).strftime("%Y-%m-%d")
    
    query = """
        INSERT INTO tokens_acceso 
        (token, en_uso, fecha_expiracion, score_puntos, vidas, modulo_actual, intentos_quiz, tiempo_estudio_min, errores_quiz) 
        VALUES (?, 0, ?, 0, 3, '1', 0, 0, 0)
    """
    exito = _ejecutar_sql_escritura(query, (token, fecha_exp))
    if not exito:
        return ""
        
    payload_remoto = {
        "token": token, "en_uso": 0, "fecha_expiracion": fecha_exp, 
        "score_puntos": 0, "vidas": 3, "modulo_actual": "1", 
        "intentos_quiz": 0, "tiempo_estudio_min": 0, "errores_quizz": 0
    }
    _supabase_rest_post("tokens_acceso", payload_remoto)
    return token

def listar_todos_los_tokens():
    query = "SELECT token, en_uso, fecha_expiracion, score_puntos, vidas, intentos_quiz, tiempo_estudio_min, errores_quiz FROM tokens_acceso"
    filas = _ejecutar_sql_lectura(query)
    
    if not filas:
        registros_nube = _supabase_rest_get_todo("tokens_acceso")
        for reg in registros_nube:
            query_insert = """
                INSERT OR IGNORE INTO tokens_acceso 
                (token, en_uso, fecha_expiracion, score_puntos, vidas, modulo_actual, intentos_quiz, tiempo_estudio_min, errores_quiz) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            _ejecutar_sql_escritura(query_insert, (
                reg.get("token"), reg.get("en_uso", 0), reg.get("fecha_expiracion"),
                reg.get("score_puntos", 0), reg.get("vidas", 3), str(reg.get("modulo_actual", "1")),
                reg.get("intentos_quiz", 0), reg.get("tiempo_estudio_min", 0), reg.get("errores_quizz", 0)
            ))
        filas = _ejecutar_sql_lectura(query)
        
    claves = ["Token", "Activo", "Expiracion", "Puntos", "Vidas", "Intentos Quiz", "Tiempo Estudio (min)", "Errores Quiz"]
    return [dict(zip(claves, f)) for f in filas]

def eliminar_token(token: str):
    query = "DELETE FROM tokens_acceso WHERE token = ?"
    exito = _ejecutar_sql_escritura(query, (token,))
    if exito:
        _supabase_rest_delete("tokens_acceso", "token", token)
