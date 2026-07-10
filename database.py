import sqlite3
import datetime
from datetime import timedelta
import streamlit as st
from supabase import create_client

# Configuración
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

def verificar_salud_sistema():
    reporte = {"status": "✅ Sistema Estable", "detalles": []}
    try:
        supabase.table("tokens_acceso").select("token").limit(1).execute()
        reporte["detalles"].append("Conexión Supabase: Activa")
    except Exception as e:
        reporte["status"] = "❌ CRÍTICO"
        reporte["detalles"].append(f"Error Supabase: {str(e)[:40]}")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT count(*) FROM tokens_acceso WHERE vidas < 0 OR score_puntos < 0")
    inc = c.fetchone()[0]
    if inc > 0: reporte["status"] = "⚠️ Alerta"; reporte["detalles"].append(f"Registros corruptos: {inc}")
    conn.close()
    return reporte

def generar_token(dias):
    token = f"MAIN-{datetime.datetime.now().strftime('%y%m%d%H%M%S')}"
    fecha_exp = (datetime.date.today() + timedelta(days=dias)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tokens_acceso VALUES (?, 0, ?, 0, 3, '1', 0, 0, 0)", (token, fecha_exp))
    conn.commit()
    conn.close()
    return token

def validar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    return True, "Ok"

def listar_todos_los_tokens():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tokens_acceso")
    res = c.fetchall()
    conn.close()
    return res

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
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET modulo_actual = ?, score_puntos = ?, vidas = ? WHERE token = ?", (str(mod), score, vidas, token))
    conn.commit()
    conn.close()

def descontar_vida_db(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = vidas - 1 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def limpiar_inconsistencias_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = 3 WHERE vidas < 0")
    c.execute("UPDATE tokens_acceso SET en_uso = 0")
    conn.commit()
    conn.close()
    return "Base saneada"

def eliminar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    
def liberar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()
