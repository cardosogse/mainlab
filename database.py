import sqlite3
import datetime
import streamlit as st
from supabase import create_client

# Configuración de Supabase
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
DB_NAME = "mainlab.db"

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso (token TEXT PRIMARY KEY, en_uso INTEGER, vidas INTEGER, score_puntos INTEGER, modulo_actual TEXT)''')
    conn.commit()
    conn.close()

def verificar_salud_sistema():
    reporte = {"status": "✅ Sistema Estable", "detalles": []}
    # Verificación Supabase
    try:
        supabase.table("tokens_acceso").select("token").limit(1).execute()
        reporte["detalles"].append("Conexión Supabase: OK")
    except Exception as e:
        reporte["status"] = "⚠️ Alerta"
        reporte["detalles"].append(f"Supabase error: {str(e)[:20]}")
    return reporte

def generar_token(dias):
    token = f"MAIN-{datetime.datetime.now().strftime('%y%m%d%H%M%S')}"
    # Guardar en Supabase
    supabase.table("tokens_acceso").insert({"token": token, "en_uso": 0, "vidas": 3}).execute()
    return token

def validar_token(token):
    res = supabase.table("tokens_acceso").select("token").eq("token", token).execute()
    return (len(res.data) > 0), ("Ok" if len(res.data) > 0 else "Inválido")

def listar_todos_los_tokens():
    res = supabase.table("tokens_acceso").select("*").execute()
    return res.data

def obtener_password_admin():
    return st.secrets["config"]["ADMIN_PASSWORD"]

def sincronizar_progreso_db(token, modulo, score, vidas):
    supabase.table("tokens_acceso").update({"modulo_actual": modulo, "score_puntos": score, "vidas": vidas}).eq("token", token).execute()

def otorgar_tiempo_extra_db(token, segundos): pass
def descontar_vida_db(token): 
    supabase.table("tokens_acceso").update({"vidas": 2}).eq("token", token).execute()

def limpiar_inconsistencias_db(): return "Saneado"
