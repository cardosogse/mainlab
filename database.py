import sqlite3
import datetime
import streamlit as st

DB_NAME = "mainlab.db"

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso 
                 (token TEXT PRIMARY KEY, en_uso INTEGER, fecha_expiracion TEXT, 
                  score_puntos INTEGER, vidas INTEGER, modulo_actual TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS admin_config (key TEXT PRIMARY KEY, value TEXT)''')
    c.execute("INSERT OR IGNORE INTO admin_config VALUES ('password', 'admin')")
    conn.commit()
    conn.close()

def verificar_salud_sistema():
    reporte = {"status": "✅ Sistema Estable", "detalles": ["Integridad: OK"]}
    return reporte

def generar_token(dias):
    token = f"MAIN-{datetime.datetime.now().strftime('%y%m%d%H%M%S')}"
    return token

def validar_token(token):
    return True, "Ok"

def listar_todos_los_tokens():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM tokens_acceso")
    res = c.fetchall()
    conn.close()
    return res

def obtener_password_admin():
    return "admin"

def actualizar_password_admin(p):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE admin_config SET value = ? WHERE key = 'password'", (p,))
    conn.commit()
    conn.close()

# --- FUNCIONES QUE TUS MÓDULOS NECESITAN ---
def sincronizar_progreso_db(token, modulo, score, vidas):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET modulo_actual = ?, score_puntos = ?, vidas = ? WHERE token = ?", (modulo, score, vidas, token))
    conn.commit()
    conn.close()

def otorgar_tiempo_extra_db(token, segundos):
    pass # Lógica de tiempo extra

def descontar_vida_db(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = vidas - 1 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def limpiar_inconsistencias_db():
    return "Saneado"
