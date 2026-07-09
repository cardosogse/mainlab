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
    st.error(f"Error de configuración: {e}")
    st.stop()

# # --- GESTIÓN DE ESTRUCTURA DE DATOS ---
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

# # --- VALIDACIÓN Y SESIÓN ---
def validar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT en_uso FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    if not res:
        conn.close()
        return False, "Token no registrado."
    if res[0] == 1:
        conn.close()
        return False, "Token ya en uso."
    elif res[0] == 2:
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

# # --- ADMINISTRACIÓN DE LICENCIAS Y SEGURIDAD ---
def generar_token(dias):
    # Genera token único usando timestamp para evitar IntegrityError
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    token = f"MAIN-{datetime.date.today().strftime('%y%m%d')}-{timestamp}"
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

def revocar_eliminar_token(token):
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

# # --- SINCRONIZACIÓN DE PROGRESO Y REGLAS DE JUEGO ---
def sincronizar_progreso_db(token, nuevos_puntos, modulo_destino):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET score_puntos = ?, modulo_actual = ? WHERE token = ?", (nuevos_puntos, modulo_destino, token))
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
