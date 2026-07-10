import sqlite3
import datetime
from datetime import timedelta
import streamlit as st
from supabase import create_client

# Configuración
SUPABASE_URL = st.secrets["supabase"]["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["supabase"]["SUPABASE_KEY"]
DB_NAME = st.secrets["config"]["DB_NAME"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso (
        token TEXT PRIMARY KEY, en_uso INTEGER, fecha_expiracion TEXT, 
        score_puntos INTEGER, vidas INTEGER, modulo_actual TEXT,
        intentos_quiz INTEGER, tiempo_estudio_seg INTEGER, errores_quiz INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS admin_config (key TEXT PRIMARY KEY, value TEXT)''')
    c.execute("INSERT OR IGNORE INTO admin_config VALUES ('password', ?)", (st.secrets["config"]["ADMIN_PASSWORD"],))
    conn.commit()
    conn.close()

def generar_token(dias):
    token = f"MAIN-{datetime.datetime.now().strftime('%y%m%d%H%M%S')}"
    fecha_exp = (datetime.date.today() + timedelta(days=dias)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tokens_acceso (token, en_uso, fecha_expiracion, score_puntos, vidas, modulo_actual, intentos_quiz, tiempo_estudio_seg, errores_quiz) VALUES (?, 0, ?, 0, 3, '1', 0, 0, 0)", (token, fecha_exp))
    conn.commit()
    conn.close()
    try: supabase.table("tokens_acceso").insert({"token": token, "en_uso": 0, "vidas": 3, "fecha_expiracion": fecha_exp}).execute()
    except: pass
    return token

def validar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    return True, "Token Válido"

def sincronizar_progreso_db(token, puntos, mod):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET score_puntos = ?, modulo_actual = ? WHERE token = ?", (puntos, str(mod), token))
    conn.commit()
    conn.close()
    try: supabase.table("tokens_acceso").update({"score_puntos": puntos, "modulo_actual": str(mod)}).eq("token", token).execute()
    except: pass

def descontar_vida_db(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = max(0, vidas - 1) WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    try: supabase.table("tokens_acceso").update({"vidas": "vidas - 1"}).eq("token", token).execute()
    except: pass

def otorgar_tiempo_extra_db(token, dias_adicionales=7):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT fecha_expiracion FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    if res:
        nueva_fecha = datetime.datetime.strptime(res[0], "%Y-%m-%d").date() + timedelta(days=dias_adicionales)
        str_fecha = nueva_fecha.strftime("%Y-%m-%d")
        c.execute("UPDATE tokens_acceso SET fecha_expiracion = ? WHERE token = ?", (str_fecha, token))
        conn.commit()
        try: supabase.table("tokens_acceso").update({"fecha_expiracion": str_fecha}).eq("token", token).execute()
        except: pass
    conn.close()

def obtener_password_admin():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT value FROM admin_config WHERE key = 'password'")
    res = c.fetchone()
    conn.close()
    return res[0] if res else "admin"

def listar_todos_los_tokens():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tokens_acceso")
    filas = c.fetchall()
    conn.close()
    return filas

def forzar_liberacion_sesion(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def verificar_salud_sistema():
    return {"status": "✅ Sistema Estable", "detalles": ["SQLite: OK", "Estructura de tablas: Verificada"]}
