import sqlite3
import datetime
from datetime import timedelta
import streamlit as st
from supabase import create_client

# # --- CONFIGURACIÓN E INICIALIZACIÓN ---
try:
    SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
    DB_NAME = st.secrets["config"]["DB_NAME"]
    ADMIN_PASSWORD = st.secrets["config"]["ADMIN_PASSWORD"]
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error de config: {e}")
    st.stop()

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso (token TEXT PRIMARY KEY, en_uso INTEGER, fecha_expiracion TEXT, score_puntos INTEGER, vidas INTEGER, modulo_actual TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS admin_config (key TEXT PRIMARY KEY, value TEXT)''')
    c.execute("INSERT OR IGNORE INTO admin_config VALUES ('password', ?)", (ADMIN_PASSWORD,))
    conn.commit()
    conn.close()

# # --- FUNCIONES MAESTRAS (Sincronizadas con tus módulos) ---
def validar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    return True, "Token Válido"

def liberar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def forzar_liberacion_sesion(token):
    liberar_token(token)

def obtener_datos_usuario(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT score_puntos, vidas, modulo_actual FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    conn.close()
    return res if res else (0, 3, 0)

def generar_token(dias):
    token = f"MAIN-{datetime.datetime.now().strftime('%y%m%d%H%M%S')}"
    fecha_exp = (datetime.date.today() + timedelta(days=dias)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tokens_acceso VALUES (?, 0, ?, 0, 3, '1')", (token, fecha_exp))
    conn.commit()
    conn.close()
    return token

def eliminar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def listar_todos_los_tokens():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tokens_acceso")
    filas = c.fetchall()
    conn.close()
    return filas

def sincronizar_progreso_db(token, nuevos_puntos, modulo_destino):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET score_puntos = ?, modulo_actual = ? WHERE token = ?", (nuevos_puntos, str(modulo_destino), token))
    conn.commit()
    conn.close()

def descontar_vida_db(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = max(0, vidas - 1) WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def otorgar_tiempo_extra_db(token, dias_adicionales=7):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT fecha_expiracion FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    if res:
        nueva_fecha = datetime.datetime.strptime(res[0], "%Y-%m-%d").date() + timedelta(days=dias_adicionales)
        c.execute("UPDATE tokens_acceso SET fecha_expiracion = ? WHERE token = ?", (nueva_fecha.strftime("%Y-%m-%d"), token))
        conn.commit()
    conn.close()

def obtener_password_admin():
    return ADMIN_PASSWORD

def actualizar_password_admin(nueva_pass):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE admin_config SET value = ? WHERE key = 'password'", (nueva_pass,))
    conn.commit()
    conn.close()
