import sqlite3
import datetime
from datetime import timedelta
import random
import string
import streamlit as st
from supabase import create_client

def obtener_llave_secreta(seccion, llave):
    if seccion in st.secrets and llave in st.secrets[seccion]:
        return st.secrets[seccion][llave].strip()
    elif llave in st.secrets:
        return st.secrets[llave].strip()
    return ""

SUPABASE_URL = obtener_llave_secreta("supabase", "SUPABASE_URL")
SUPABASE_KEY = obtener_llave_secreta("supabase", "SUPABASE_KEY")
DB_NAME = obtener_llave_secreta("config", "DB_NAME") or "mainlab.db"

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL else None
except Exception:
    supabase = None

def inicializar_db():
    """Garantiza la creación y migración progresiva de la base de datos en disco."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso (
            token TEXT PRIMARY KEY, en_uso INTEGER, fecha_expiracion TEXT, 
            score_puntos INTEGER, vidas INTEGER, modulo_actual TEXT,
            intentos_quiz INTEGER, tiempo_estudio_min INTEGER, errores_quiz INTEGER)''')
        
        # ESCUDO DE MIGRACIÓN: Detecta tablas antiguas y añade las columnas analíticas faltantes
        c.execute("PRAGMA table_info(tokens_acceso)")
        columnas_existentes = [col[1] for col in c.fetchall()]
        
        columnas_nuevas = {
            "intentos_quiz": "INTEGER DEFAULT 0",
            "tiempo_estudio_min": "INTEGER DEFAULT 0",
            "errores_quiz": "INTEGER DEFAULT 0"
        }
        
        for col_nombre, col_tipo in columnas_nuevas.items():
            if col_nombre not in columnas_existentes:
                c.execute(f"ALTER TABLE tokens_acceso ADD COLUMN {col_nombre} {col_tipo}")
        conn.commit()

def obtener_password_admin():
    return obtener_llave_secreta("config", "ADMIN_PASSWORD") or "ADMIN123"

def validar_token(token: str):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT score_puntos, vidas, modulo_actual, errores_quiz, tiempo_estudio_min, fecha_expiracion FROM tokens_acceso WHERE token = ?", (token,))
            res = c.fetchone()
            
        if res:
            score, vidas, modulo, errores, tiempo_min, fecha_exp = res
            if datetime.date.today().strftime("%Y-%m-%d") > fecha_exp:
                return False, "expired"
            return True, {"puntos": score, "vidas": vidas, "modulo": modulo, "errores": errores, "tiempo": tiempo_min}
    except sqlite3.Error as e:
        st.error(f"Fallo crítico en capa de datos local: {str(e)}")
    return False, "invalid"

def sincronizar_progreso_db(token: str, puntos: int, mod: str, vidas: int, tiempo_min: int):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("UPDATE tokens_acceso SET score_puntos = ?, modulo_actual = ?, vidas = ?, tiempo_estudio_min = ? WHERE token = ?", 
                      (int(puntos), str(mod), int(vidas), int(tiempo_min), token))
            conn.commit()
            
        if supabase:
            try:
                supabase.table("tokens_acceso").update({
                    "score_puntos": int(puntos), "modulo_actual": str(mod), "vidas": int(vidas), "tiempo_estudio_min": int(tiempo_min)
                }).eq("token", token).execute()
            except Exception:
                pass
    except sqlite3.Error:
        pass

def guardar_registro_juego(alumno_id: str, dia_modulo: int, puntaje: int, precision_pct: int, metadata_juego: dict):
    if not supabase: return False
    payload = {
        "alumno_id": alumno_id, "dia_modulo": int(dia_modulo), "puntaje": int(puntaje),
        "precision_pct": int(precision_pct), "metadata_juego": metadata_juego
    }
    try:
        supabase.table("historial_juegos").insert(payload).execute()
        return True
    except Exception:
        return False

def generar_token(dias: int) -> str:
    """Generates a token completely decoupled from the UI layer."""
    token = f"ML-{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
    fecha_exp = (datetime.date.today() + timedelta(days=dias)).strftime("%Y-%m-%d")
    
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO tokens_acceso VALUES (?, 0, ?, 0, 3, '1', 0, 0, 0)", (token, fecha_exp))
            conn.commit()
    except sqlite3.Error as e:
        st.error(f"Error al generar licencia en almacenamiento local: {str(e)}")
        return ""
        
    if supabase:
        try:
            payload_remoto = {
                "token": token, "en_uso": 0, "fecha_expiracion": fecha_exp, 
                "score_puntos": 0, "vidas": 3, "modulo_actual": "1", 
                "intentos_quiz": 0, "tiempo_estudio_min": 0, "errores_quiz": 0
            }
            supabase.table("tokens_acceso").insert(payload_remoto).execute()
        except Exception:
            pass
            
    return token

def listar_todos_los_tokens():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT token, en_uso, fecha_expiracion, score_puntos, vidas, intentos_quiz, tiempo_estudio_min, errores_quiz FROM tokens_acceso")
            filas = c.fetchall()
        claves = ["Token", "Activo", "Expiracion", "Puntos", "Vidas", "Intentos Quiz", "Tiempo Estudio (min)", "Errores Quiz"]
        return [dict(zip(claves, f)) for f in filas]
    except sqlite3.Error:
        return []

def eliminar_token(token: str):
    try:
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token,))
            conn.commit()
        if supabase:
            try:
                supabase.table("tokens_acceso").delete().eq("token", token).execute()
            except Exception:
                pass
    except sqlite3.Error as e:
        st.error(f"No se pudo eliminar la licencia de la matriz: {str(e)}")
