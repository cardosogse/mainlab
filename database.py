import sqlite3
import datetime
from datetime import timedelta
import streamlit as st
from supabase import create_client

# --- CONFIGURACIÓN ---
DB_NAME = "licencias.db"
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- FUNCIONES DE SUPABASE (Nube) ---
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

# --- FUNCIONES DE LICENCIAS (SQLITE - LO QUE TU APP NECESITA) ---
def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Tabla de licencias
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso 
                 (token TEXT PRIMARY KEY, en_uso INTEGER, fecha_expiracion TEXT, 
                  score_puntos INTEGER, vidas INTEGER, modulo_actual TEXT)''')
    # Tabla para contraseñas de admin (que tu app pide)
    c.execute('''CREATE TABLE IF NOT EXISTS admin_config (key TEXT PRIMARY KEY, value TEXT)''')
    # Valor inicial si no existe
    c.execute("INSERT OR IGNORE INTO admin_config VALUES ('password', 'admin123')")
    conn.commit()
    conn.close()

def validar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tokens_acceso WHERE token = ? AND en_uso = 0", (token,))
    res = c.fetchone()
    if res:
        c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token,))
        conn.commit()
        conn.close()
        return True, "Token Válido"
    conn.close()
    return False, "Token no registrado o en uso."

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
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT value FROM admin_config WHERE key = 'password'")
    res = c.fetchone()
    conn.close()
    return res[0] if res else "admin123"

def actualizar_password_admin(nueva_pass):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE admin_config SET value = ? WHERE key = 'password'", (nueva_pass,))
    conn.commit()
    conn.close()

# --- FUNCIONES DE MANTENIMIENTO ---
def liberar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def forzar_liberacion_sesion(token):
    liberar_token(token)

def revocar_eliminar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def listar_todos_los_tokens():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT token, en_uso, fecha_expiracion, score_puntos, vidas, modulo_actual FROM tokens_acceso")
    filas = c.fetchall()
    conn.close()
    return filas
