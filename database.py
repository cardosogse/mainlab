import sqlite3
import datetime
from datetime import timedelta
import streamlit as st
from supabase import create_client

# --- CONFIGURACIÓN ---
DB_NAME = "licencias.db"  # Asegúrate de que este sea el nombre de tu archivo DB
supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

# --- FUNCIONES DE SUPABASE (Almacén en la Nube) ---
def guardar_progreso(username, datos):
    try:
        supabase.table("usuarios").insert({
            "username": username, 
            "progreso": str(datos)
        }).execute()
        return True
    except Exception as e:
        st.error(f"Error al sincronizar con la nube: {e}")
        return False

def obtener_progreso(username):
    try:
        response = supabase.table("usuarios").select("progreso").eq("username", username).execute()
        if response.data:
            return response.data[0]["progreso"]
        return None
    except Exception:
        return None

# --- FUNCIONES DE LICENCIAS (SQLite Local) ---
# ... (Aquí va todo tu código de licencias original que me pasaste) ...
def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Asegúrate de que esta línea cree tu tabla de licencias original
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso 
                 (token TEXT PRIMARY KEY, en_uso INTEGER, fecha_expiracion TEXT, 
                  score_puntos INTEGER, vidas INTEGER, modulo_actual TEXT)''')
    conn.commit()
    conn.close()

def liberar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def forzar_liberacion_sesion(token):
    liberar_token(token)

def revocar_eliminar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def listar_todos_los_tokens():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT token, en_uso, fecha_expiracion, score_puntos, vidas, modulo_actual FROM tokens_acceso")
    filas = c.fetchall()
    conn.close()
    
    datos_limpios = []
    for f in filas:
        token, en_uso, f_exp, pts, vds, mod = f
        try:
            date_obj = datetime.datetime.strptime(f_exp, "%Y-%m-%d").date()
            dias_restantes = (date_obj - datetime.date.today()).days
            dias_str = f"{dias_restantes} días" if dias_restantes >= 0 else "Expirado"
        except:
            dias_str = "Indefinido"
        
        estado_uso = "En uso" if en_uso else "Libre"
        datos_limpios.append((token, estado_uso, dias_str, pts, vds, f"Módulo {mod}"))
    return datos_limpios

def sincronizar_progreso_db(token, nuevos_puntos, modulo_destino):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET score_puntos = ?, modulo_actual = ? WHERE token = ?", (nuevos_puntos, modulo_destino, token))
    conn.commit()
    conn.close()

def descontar_vida_db(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET vidas = max(0, vidas - 1) WHERE token = ?", (token,))
    conn.commit()
    conn.close()

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
