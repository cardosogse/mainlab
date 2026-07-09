import sqlite3
import datetime
from datetime import timedelta
import streamlit as st
from supabase import create_client

# --- 1. CONFIGURACIÓN ---
try:
    SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
    DB_NAME = st.secrets["config"]["DB_NAME"]
    ADMIN_PASSWORD = st.secrets["config"]["ADMIN_PASSWORD"]
except KeyError as e:
    st.error(f"Error crítico: Falta la configuración {e} en los Secrets.")
    st.stop()

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error conectando a Supabase: {e}")
    st.stop()

# --- FUNCIONES DE SUPABASE ---
def guardar_progreso(username, datos):
    try:
        supabase.table("usuarios").insert({"username": username, "progreso": str(datos)}).execute()
        return True
    except Exception: return False

def obtener_progreso(username):
    try:
        response = supabase.table("usuarios").select("progreso").eq("username", username).execute()
        return response.data[0]["progreso"] if response.data else None
    except Exception: return None

# --- FUNCIONES DE SQLITE ---
def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso 
                  (token TEXT PRIMARY KEY, en_uso INTEGER, fecha_expiracion TEXT, 
                   score_puntos INTEGER, vidas INTEGER, modulo_actual TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS admin_config (key TEXT PRIMARY KEY, value TEXT)''')
    c.execute("INSERT OR IGNORE INTO admin_config VALUES ('password', ?)", (ADMIN_PASSWORD,))
    conn.commit()
    conn.close()

def validar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT en_uso FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    if not res:
        conn.close()
        return False, "Token no registrado."
    estado = res[0]
    if estado == 1:
        conn.close()
        return False, "Token ya en uso."
    elif estado == 2:
        conn.close()
        return False, "Este token ha sido revocado."
    c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    return True, "Token Válido"

def obtener_datos_usuario(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT score_puntos, vidas, modulo_actual FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    conn.close()
    return res if res else (0, 3, 0)

def generar_token(dias):
    token = f"MAIN-{datetime.date.today().strftime('%y%m%d')}"
    fecha_exp = (datetime.date.today() + timedelta(days=dias)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tokens_acceso VALUES (?, 0, ?, 0, 3, '1')", (token, fecha_exp))
    conn.commit()
    conn.close()
    return token

def obtener_password_admin():
    return ADMIN_PASSWORD

def actualizar_password_admin(nueva_pass):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE admin_config SET value = ? WHERE key = 'password'", (nueva_pass,))
    conn.commit()
    conn.close()

def liberar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def forzar_liberacion_sesion(token):
    liberar_token(token)

def revocar_token_logico(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 2 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def listar_todos_los_tokens():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT token, en_uso, fecha_expiracion, score_puntos, vidas, modulo_actual FROM tokens_acceso")
    filas = c.fetchall()
    conn.close()
    return filas
