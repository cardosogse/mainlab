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
                  fecha_expiracion DATE, 
                  en_uso BOOLEAN, 
                  identificador_usuario TEXT,
                  modulo_actual INTEGER DEFAULT 1,
                  score_puntos INTEGER DEFAULT 0,
                  vidas INTEGER DEFAULT 3)''')
    
    # Tabla persistente para configuraciones avanzadas del sistema
    c.execute('''CREATE TABLE IF NOT EXISTS config_sistema
                 (clave TEXT PRIMARY KEY, valor TEXT)''')
    
    # Contraseña por defecto si la tabla está vacía
    c.execute("INSERT OR IGNORE INTO config_sistema (clave, valor) VALUES ('admin_password', 'UNAM2026')")
    
    token_prueba = "SYNAPSIS-PRO-2026"
    fecha_futura = datetime.date.today() + timedelta(days=30)
    c.execute("INSERT OR IGNORE INTO tokens_acceso (token, fecha_expiracion, en_uso, identificador_usuario, modulo_actual, score_puntos, vidas) VALUES (?, ?, ?, ?, 1, 0, 3)", 
              (token_prueba, fecha_futura, False, "Admin"))
    conn.commit()
    conn.close()

# --- FUNCIONES DE GESTIÓN DE CONTRASEÑA ---
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
    c.execute("UPDATE config_sistema SET valor = ? WHERE clave = 'admin_password'", (nueva_pass.strip(),))
    conn.commit()
    conn.close()

# --- REINGENIERÍA DE LICENCIAS DINÁMICAS (CORTAS) ---
def generar_token(vigencia_dias):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    caracteres = string.ascii_uppercase + string.digits
    
    # Condicional de segmentación de cupones cortos aprobado
    if vigencia_dias >= 90:
        prefix = "MLP-"
    else:
        prefix = "ML-"
        
    nuevo_tok = prefix + "".join(random.choice(caracteres) for _ in range(6))
    exp = datetime.date.today() + timedelta(days=vigencia_dias)
    c.execute("INSERT INTO tokens_acceso (token, fecha_expiracion, en_uso, identificador_usuario, modulo_actual, score_puntos, vidas) VALUES (?, ?, 0, 'Estudiante Autónomo', 1, 0, 3)", 
              (nuevo_tok, exp))
    conn.commit()
    conn.close()
    return nuevo_tok

def obtener_datos_usuario(token):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT score_puntos, vidas, modulo_actual FROM tokens_acceso WHERE token = ?", (token,))
    res = f = c.fetchone()
    conn.close()
    return res if res else (0, 3, 1)

def validar_token(token_ingresado):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT fecha_expiracion, en_uso FROM tokens_acceso WHERE token = ?", (token_ingresado.strip().upper(),))
    resultado = c.fetchone()
    
    if resultado:
        fecha_exp = datetime.datetime.strptime(resultado[0], "%Y-%m-%d").date()
        en_uso = resultado[1]
        if datetime.date.today() > fecha_exp:
            conn.close()
            return False, "El token ha expirado o fue cancelado por el administrador."
        if en_uso:
            conn.close()
            return False, "Acceso denegado: Token activo en otro dispositivo."
        conn.close()
        return True, "Token Válido"
    conn.close()
    return False, "Token no registrado en el servidor central de licencias."

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
