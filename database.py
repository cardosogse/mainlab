import sqlite3
import datetime
from datetime import timedelta
import streamlit as st
from supabase import create_client

# Configuración
DB_NAME = "mainlab.db"

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso (token TEXT PRIMARY KEY, en_uso INTEGER, vidas INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS admin_config (key TEXT PRIMARY KEY, value TEXT)''')
    c.execute("INSERT OR IGNORE INTO admin_config VALUES ('password', 'admin')")
    conn.commit()
    conn.close()

def verificar_salud_sistema():
    reporte = {"status": "✅ Sistema Estable", "detalles": []}
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.close()
        reporte["detalles"].append("Base de datos local: OK")
    except Exception as e:
        reporte["status"] = "❌ CRÍTICO"
        reporte["detalles"].append(str(e))
    return reporte

def generar_token(dias):
    token = f"MAIN-{datetime.datetime.now().strftime('%y%m%d%H%M%S')}"
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tokens_acceso VALUES (?, 0, 3)", (token,))
    conn.commit()
    conn.close()
    return token

def validar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT token FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    conn.close()
    return (res is not None), ("Ok" if res else "Token inválido")

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
    return res[0] if res else "admin"

def actualizar_password_admin(p):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE admin_config SET value = ? WHERE key = 'password'", (p,))
    conn.commit()
    conn.close()
