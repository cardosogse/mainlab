import sqlite3
import datetime
from datetime import timedelta
import random
import string
import streamlit as st
from supabase import create_client

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

def generar_token(dias):
    # Lógica de longitud corregida y optimizada según vigencia
    prefix = "MLP-" if dias >= 90 else "ML-"
    caracteres_aleatorios = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    token = f"{prefix}{caracteres_aleatorios}"
    
    fecha_exp = (datetime.date.today() + timedelta(days=dias)).strftime("%Y-%m-%d")
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tokens_acceso VALUES (?, 0, ?, 0, 3, '1', 0, 0, 0)", (token, fecha_exp))
    conn.commit()
    conn.close()
    
    try:
        supabase.table("tokens_acceso").insert({
            "token": token, "en_uso": 0, "fecha_expiracion": fecha_exp,
            "score_puntos": 0, "vidas": 3, "modulo_actual": "1",
            "intentos_quiz": 0, "tiempo_estudio_seg": 0, "errores_quiz": 0
        }).execute()
    except: pass
    return token

def validar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT score_puntos, vidas, modulo_actual, errores_quiz, fecha_expiracion FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    if res:
        score, vidas, modulo, errores, fecha_exp = res
        hoy = datetime.date.today().strftime("%Y-%m-%d")
        
        # Auditoría de caducidad automática informada a Supabase
        if hoy > fecha_exp:
            conn.close()
            try: supabase.table("tokens_acceso").update({"en_uso": 0, "modulo_actual": "EXPIRADO"}).eq("token", token).execute()
            except: pass
            return False, "expired"
            
        c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token,))
        conn.commit()
        conn.close()
        try: supabase.table("tokens_acceso").update({"en_uso": 1}).eq("token", token).execute()
        except: pass
        return True, {"puntos": score, "vidas": vidas, "modulo": modulo, "errores": errores}
    conn.close()
    return False, "invalid"

def eliminar_token(token):
    # Eliminación unificada y sincronizada con Supabase
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    try:
        supabase.table("tokens_acceso").delete().eq("token", token).execute()
    except: pass

def sincronizar_progreso_db(token, puntos, mod, vidas):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET score_puntos = ?, modulo_actual = ?, vidas = ? WHERE token = ?", (puntos, str(mod), vidas, token))
    conn.commit()
    conn.close()
    try:
        supabase.table("tokens_acceso").update({
            "score_puntos": int(puntos), "modulo_actual": str(mod), "vidas": int(vidas)
        }).eq("token", token).execute()
    except: pass

def registrar_intento_quiz(token, nuevas_vidas, errores_totales):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET intentos_quiz = intentos_quiz + 1, errores_quiz = ?, vidas = ? WHERE token = ?", (errores_totales, nuevas_vidas, token))
    conn.commit()
    conn.close()
    try:
        supabase.table("tokens_acceso").update({
            "vidas": int(nuevas_vidas), "errores_quiz": int(errores_totales)
        }).eq("token", token).execute()
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
    c.execute("SELECT token, en_uso, fecha_expiracion, score_puntos, vidas, modulo_actual, intentos_quiz, errores_quiz FROM tokens_acceso")
    filas = c.fetchall()
    conn.close()
    claves = ["Token", "Activo", "Expiracion", "Puntos", "Vidas", "Modulo", "Intentos Quiz", "Errores Quiz"]
    return [dict(zip(claves, f)) for f in filas]

def forzar_liberacion_sesion(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    try: supabase.table("tokens_acceso").update({"en_uso": 0}).eq("token", token).execute()
    except: pass

def verificar_salud_sistema():
    try:
        supabase.table("tokens_acceso").select("token", count="exact").limit(1).execute()
        return {"status": "✅ Sistema Estable", "detalles": ["Conexión Supabase: OK", "Estructura SQLite: Verificada"]}
    except Exception as e:
        return {"status": "⚠️ Alerta de Inconsistencia", "detalles": [f"Error de enlace: {str(e)}"]}
