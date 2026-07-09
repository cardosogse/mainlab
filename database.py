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
    
    # Actualizar local y nube
    c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    try:
        supabase.table("tokens_acceso").update({"en_uso": 1}).eq("token", token).execute()
    except: pass
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
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    token = f"MAIN-{datetime.date.today().strftime('%y%m%d')}-{timestamp}"
    fecha_exp = (datetime.date.today() + timedelta(days=dias)).strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tokens_acceso VALUES (?, 0, ?, 0, 3, '1')", (token, fecha_exp))
    conn.commit()
    conn.close()
    
    try:
        supabase.table("tokens_acceso").insert({
            "token": token, "en_uso": 0, "fecha_expiracion": fecha_exp, 
            "score_puntos": 0, "vidas": 3, "modulo_actual": '1'
        }).execute()
    except: pass
    return token

def revocar_eliminar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 2 WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    try:
        supabase.table("tokens_acceso").update({"en_uso": 2}).eq("token", token).execute()
    except: pass

def liberar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    try:
        supabase.table("tokens_acceso").update({"en_uso": 0}).eq("token", token).execute()
    except: pass

# # --- SINCRONIZACIÓN DE PROGRESO ---
def sincronizar_progreso_db(token, nuevos_puntos, modulo_destino):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET score_puntos = ?, modulo_actual = ? WHERE token = ?", (nuevos_puntos, modulo_destino, token))
    conn.commit()
    conn.close()
    try:
        supabase.table("tokens_acceso").update({"score_puntos": nuevos_puntos, "modulo_actual": str(modulo_destino)}).eq("token", token).execute()
    except: pass

def descontar_vida_db(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = max(0, vidas - 1) WHERE token = ?", (token,))
    # Obtener valor nuevo para sync
    c.execute("SELECT vidas FROM tokens_acceso WHERE token = ?", (token,))
    nuevas_vidas = c.fetchone()[0]
    conn.commit()
    conn.close()
    try:
        supabase.table("tokens_acceso").update({"vidas": nuevas_vidas}).eq("token", token).execute()
    except: pass

def otorgar_tiempo_extra_db(token, dias_adicionales=7):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT fecha_expiracion FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    if res:
        nueva_fecha = datetime.datetime.strptime(res[0], "%Y-%m-%d").date() + timedelta(days=dias_adicionales)
        fecha_str = nueva_fecha.strftime("%Y-%m-%d")
        c.execute("UPDATE tokens_acceso SET fecha_expiracion = ? WHERE token = ?", (fecha_str, token))
        conn.commit()
        try:
            supabase.table("tokens_acceso").update({"fecha_expiracion": fecha_str}).eq("token", token).execute()
        except: pass
    conn.close()
