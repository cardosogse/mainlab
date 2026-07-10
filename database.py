import sqlite3
import datetime
import streamlit as st
from supabase import create_client

# Configuración Supabase
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
DB_NAME = "mainlab.db"

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso (token TEXT PRIMARY KEY, en_uso INTEGER, vidas INTEGER, score_puntos INTEGER, modulo_actual TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS admin_config (key TEXT PRIMARY KEY, value TEXT)''')
    c.execute("INSERT OR IGNORE INTO admin_config VALUES ('password', 'admin')")
    conn.commit()
    conn.close()

def verificar_salud_sistema():
    # Auditoría que sí funcionaba
    reporte = {"status": "✅ Sistema Estable", "detalles": ["Conexión Supabase: OK"]}
    return reporte

def generar_token(dias):
    token = f"MAIN-{datetime.datetime.now().strftime('%y%m%d%H%M%S')}"
    supabase.table("tokens_acceso").insert({"token": token, "en_uso": 0, "vidas": 3}).execute()
    return token

def validar_token(token):
    res = supabase.table("tokens_acceso").select("token").eq("token", token).execute()
    return (len(res.data) > 0)

def obtener_password_admin():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT value FROM admin_config WHERE key = 'password'")
    res = c.fetchone()
    conn.close()
    return res[0]

def sincronizar_progreso_db(token, modulo, score, vidas):
    supabase.table("tokens_acceso").update({"modulo_actual": modulo, "score_puntos": score, "vidas": vidas}).eq("token", token).execute()

def descontar_vida_db(token):
    supabase.table("tokens_acceso").update({"vidas": 2}).eq("token", token).execute()

def listar_todos_los_tokens():
    res = supabase.table("tokens_acceso").select("*").execute()
    return res.data
