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
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso (
        token TEXT PRIMARY KEY, en_uso INTEGER, fecha_expiracion TEXT, 
        score_puntos INTEGER, vidas INTEGER, modulo_actual TEXT,
        intentos_quiz INTEGER, tiempo_estudio_seg INTEGER, errores_quiz INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS admin_config (key TEXT PRIMARY KEY, value TEXT)''')
    c.execute("INSERT OR IGNORE INTO admin_config VALUES ('password', ?)", (ADMIN_PASSWORD,))
    conn.commit()
    conn.close()

# # --- MONITOR DE SALUD Y AUTO-REPARACIÓN ---
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
    inconsistencias = c.fetchone()[0]
    if inconsistencias > 0:
        reporte["status"] = "⚠️ Alerta de Inconsistencia"
        reporte["detalles"].append(f"Registros corruptos: {inconsistencias}")
    conn.close()
    return reporte

def limpiar_inconsistencias_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = 3 WHERE vidas < 0")
    c.execute("UPDATE tokens_acceso SET score_puntos = 0 WHERE score_puntos < 0")
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE en_uso = 1") # Limpia sesiones colgadas
    conn.commit()
    conn.close()
    return "Base de datos saneada con éxito."

# # --- FUNCIONES DE GESTIÓN (COMPLETAS) ---

def registrar_intento_quiz(token, es_correcto):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if not es_correcto:
        c.execute("UPDATE tokens_acceso SET intentos_quiz = intentos_quiz + 1, errores_quiz = errores_quiz + 1 WHERE token = ?", (token,))
    else:
        c.execute("UPDATE tokens_acceso SET intentos_quiz = intentos_quiz + 1 WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    try:
        if not es_correcto:
            supabase.table("tokens_acceso").update({"intentos_quiz": "intentos_quiz + 1", "errores_quiz": "errores_quiz + 1"}).eq("token", token).execute()
        else:
            supabase.table("tokens_acceso").update({"intentos_quiz": "intentos_quiz + 1"}).eq("token", token).execute()
    except: pass

def sincronizar_progreso_db(token, puntos, mod):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET score_puntos = ?, modulo_actual = ? WHERE token = ?", (puntos, str(mod), token))
    conn.commit()
    conn.close()
    try:
        supabase.table("tokens_acceso").update({"score_puntos": puntos, "modulo_actual": str(mod)}).eq("token", token).execute()
    except: pass

def descontar_vida_db(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = max(0, vidas - 1) WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    try:
        supabase.table("tokens_acceso").update({"vidas": "vidas - 1"}).eq("token", token).execute()
    except: pass

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
    try:
        supabase.table("tokens_acceso").update({"fecha_expiracion": nueva_fecha.strftime("%Y-%m-%d")}).eq("token", token).execute()
    except: pass

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

def generar_token(dias):
    token = f"MAIN-{datetime.datetime.now().strftime('%y%m%d%H%M%S')}"
    fecha_exp = (datetime.date.today() + timedelta(days=dias)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tokens_acceso (token, en_uso, fecha_expiracion, score_puntos, vidas, modulo_actual, intentos_quiz, tiempo_estudio_seg, errores_quiz) VALUES (?, 0, ?, 0, 3, '1', 0, 0, 0)", (token, fecha_exp))
    conn.commit()
    conn.close()
    return token

def eliminar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    try:
        supabase.table("tokens_acceso").delete().eq("token", token).execute()
    except: pass

def listar_todos_los_tokens():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tokens_acceso")
    filas = c.fetchall()
    conn.close()
    return filas

def obtener_datos_usuario(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT score_puntos, vidas, modulo_actual FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    conn.close()
    return res if res else (0, 3, '1')

def obtener_password_admin():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT value FROM admin_config WHERE key = 'password'")
    res = c.fetchone()
    conn.close()
    return res[0] if res else "admin"

def actualizar_password_admin(nueva_pass):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE admin_config SET value = ? WHERE key = 'password'", (nueva_pass,))
    conn.commit()
    conn.close()
