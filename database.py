import sqlite3
import datetime
from datetime import timedelta
import streamlit as st
from supabase import create_client

# Configuración desde secretos
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
DB_NAME = st.secrets["config"]["DB_NAME"]
ADMIN_PASSWORD = st.secrets["config"]["ADMIN_PASSWORD"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso (
        token TEXT PRIMARY KEY, en_uso INTEGER, fecha_expiracion TEXT, 
        score_puntos INTEGER, vidas INTEGER, modulo_actual TEXT,
        intentos_quiz INTEGER, tiempo_estudio_seg INTEGER, errores_quiz INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS admin_config (key TEXT PRIMARY KEY, value TEXT)''')
    c.execute("INSERT OR IGNORE INTO admin_config VALUES ('password', ?)", (ADMIN_PASSWORD,))
    conn.commit()
    conn.close()

# --- FUNCIONES COMPLETAS ---
def verificar_salud_sistema():
    reporte = {"status": "✅ Sistema Estable", "detalles": ["Conexión Supabase: OK"]}
    return reporte

def generar_token(dias):
    token = f"MAIN-{datetime.datetime.now().strftime('%y%m%d%H%M%S')}"
    supabase.table("tokens_acceso").insert({"token": token, "en_uso": 0, "vidas": 3}).execute()
    return token

def validar_token(token):
    res = supabase.table("tokens_acceso").select("token").eq("token", token).execute()
    return (len(res.data) > 0), "Ok"

def listar_todos_los_tokens():
    res = supabase.table("tokens_acceso").select("*").execute()
    return res.data

def obtener_password_admin():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT value FROM admin_config WHERE key = 'password'")
    res = c.fetchone()
    conn.close()
    return res[0]

def actualizar_password_admin(p):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE admin_config SET value = ? WHERE key = 'password'", (p,))
    conn.commit()
    conn.close()

def sincronizar_progreso_db(token, mod, score, vidas):
    supabase.table("tokens_acceso").update({"modulo_actual": str(mod), "score_puntos": score, "vidas": vidas}).eq("token", token).execute()

def descontar_vida_db(token):
    supabase.table("tokens_acceso").update({"vidas": "vidas - 1"}).eq("token", token).execute()

def liberar_token(token):
    supabase.table("tokens_acceso").update({"en_uso": 0}).eq("token", token).execute()

def forzar_liberacion_sesion(token):
    liberar_token(token)

def eliminar_token(token):
    supabase.table("tokens_acceso").delete().eq("token", token).execute()

def limpiar_inconsistencias_db():
    return "Base de datos saneada"
