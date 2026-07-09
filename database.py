# === ARCHIVO COMPLETO: database.py ===
import sqlite3
import datetime
from datetime import timedelta
import random
import string

# Nombre original para romper el Write-Lock en Streamlit Cloud
DB_NAME = 'mainlab_pro_auth.db'

def inicializar_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tokens_acceso
                 (token TEXT PRIMARY KEY, 
                  fecha_expiracion DATE, \
                  en_uso BOOLEAN, \
                  identificador_usuario TEXT, \
                  modulo_actual INTEGER DEFAULT 1, \
                  score_puntos INTEGER DEFAULT 0, \
                  vidas INTEGER DEFAULT 3)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS config_sistema
                 (clave TEXT PRIMARY KEY, valor TEXT)''')
    
    c.execute("INSERT OR IGNORE INTO config_sistema (clave, valor) VALUES ('admin_password', 'UNAM2026')")
    
    token_prueba = "SYNAPSIS-PRO-2026"
    fecha_futura = datetime.date.today() + timedelta(days=30)
    c.execute("INSERT OR IGNORE INTO tokens_acceso (token, fecha_expiracion, en_uso, identificador_usuario, modulo_actual, score_puntos, vidas) VALUES (?, ?, ?, ?, 1, 0, 3)", 
              (token_prueba, fecha_futura, False, "Admin"))
    conn.commit()
    conn.close()

def obtener_password_admin():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT valor FROM config_sistema WHERE clave = 'admin_password'")
    res = c.fetchone()
    conn.close()
    return res[0] if res else "UNAM2026"

def actualizar_password_admin(nueva_pass):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE config_sistema SET valor = ? WHERE clave = 'admin_password'", (nueva_pass,))
    conn.commit()
    conn.close()

def validar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Blindaje contra SQLi usando parámetros puros (?)
    c.execute("SELECT en_uso, fecha_expiracion, identificador_usuario, modulo_actual, score_puntos, vidas FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    
    if not res:
        conn.close()
        return False, "", 1, 0, 3
        
    en_uso, f_exp, usuario, modulo, pts, vds = res
    
    try:
        date_obj = datetime.datetime.strptime(f_exp, "%Y-%m-%d").date()
        if date_obj < datetime.date.today():
            conn.close()
            return False, "", 1, 0, 3
    except:
        pass

    if en_uso:
        conn.close()
        return False, "", 1, 0, 3
        
    c.execute("UPDATE tokens_acceso SET en_uso = 1 WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    return True, usuario, modulo, pts, vds

def liberar_token(token):
    if not token: return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def forzar_liberacion_sesion(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tokens_acceso SET en_uso = 0 WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def revocar_eliminar_token(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tokens_acceso WHERE token = ?", (token,))
    conn.commit()
    conn.close()

def generar_token(dias_vigencia, usuario_id):
    caracteres = string.ascii_uppercase + string.digits
    sufijo = ''.join(random.choices(caracteres, k=4))
    nuevo_token = f"SYNAPSIS-PRO-{sufijo}"
    fecha_exp = datetime.date.today() + timedelta(days=dias_vigencia)
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tokens_acceso (token, fecha_expiracion, en_uso, identificador_usuario, modulo_actual, score_puntos, vidas) VALUES (?, ?, 0, ?, 1, 0, 3)", 
              (nuevo_token, str(fecha_exp), usuario_id))
    conn.commit()
    conn.close()
    return nuevo_token

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
        try:
            curr_date = datetime.datetime.strptime(res[0], "%Y-%m-%d").date()
            nueva_fecha = curr_date + timedelta(days=dias_adicionales)
            c.execute("UPDATE tokens_acceso SET fecha_expiracion = ? WHERE token = ?", (str(nueva_fecha), token))
            conn.commit()
        except:
            pass
    conn.close()

def obtener_datos_usuario(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT identificador_usuario, modulo_actual, score_puntos, vidas FROM tokens_acceso WHERE token = ?", (token,))
    res = c.fetchone()
    conn.close()
    return res if res else (None, 1, 0, 3)
