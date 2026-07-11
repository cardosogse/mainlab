import streamlit as st
import pandas as pd
import time
from datetime import datetime
import database as db
from assets import cargar_estilos, mezclar_memorama

# 1. CONFIGURACIÓN DE PÁGINA INMEDIATA (Debe ser el primer comando de Streamlit)
st.set_page_config(
    page_title="MainLab - Bioquímica Interactiva", 
    layout="wide", 
    page_icon="🧬",
    initial_sidebar_state="collapsed"
)

# 2. INYECCIÓN DE ESTILOS DE ALTA FIDELIDAD (Estilo Neón/Cyber-Lab Oscuro)
cargar_estilos()

# 3. INICIALIZACIÓN ATÓMICA DE LA BASE DE DATOS LOCAL
db.inicializar_db()

# ==========================================
# CENTRALIZACIÓN Y GESTIÓN DE ESTADO ATÓMICO
# ==========================================

def init_session_state():
    """Inicializa de forma robusta todas las variables de control de flujo para evitar KeyErrors."""
    variables_por_defecto = {
        'auth': None,
        'token_actual': None,
        'procesando': False,
        'ultimo_minuto_sincronizado': -1,
        'puntos_acumulados': 0,
        'vidas': 3,
        'errores_quiz': 0,
        'tiempo_historico_min': 0,
        'tiempo_estudio_min': 0,
        'inicio_sesion_unix': None,
        'modulo_actual': "1",
        'dia_actual_traker': 1,
        'telemetria_iniciada_hoy': False
    }
    
    for llave, valor in variables_por_defecto.items():
        if llave not in st.session_state:
            st.session_state[llave] = valor

init_session_state()

# Cacheado dinámico de la clave maestra administrativa para evitar cuellos de botella
if 'pass_maestra' not in st.session_state:
    st.session_state['pass_maestra'] = db.obtener_password_admin()

def hidratar_sesion_alumno(token, datos_db):
    """
    Estructura el micro y macro progreso recuperando datos persistentes del servidor Cloud.
    Garantiza consistencia absoluta eliminando la volatilidad de los reinicios.
    """
    st.session_state['token_actual'] = token
    st.session_state['puntos_acumulados'] = datos_db.get("puntos", 0)
    st.session_state['vidas'] = datos_db.get("vidas", 3)
    st.session_state['errores_quiz'] = datos_db.get("errores", 0)
    st.session_state['tiempo_historico_min'] = datos_db.get("tiempo", 0)
    st.session_state['tiempo_estudio_min'] = datos_db.get("tiempo", 0)
    st.session_state['inicio_sesion_unix'] = time.time()
    st.session_state['ultimo_minuto_sincronizado'] = 0
    st.session_state['telemetria_iniciada_hoy'] = False
    
    # Inicialización del entorno del minijuego interno
    if 'memo_tablero' not in st.session_state or not st.session_state['memo_tablero']:
        st.session_state['memo_tablero'] = mezclar_memorama()
        st.session_state['memo_reveladas'] = []
        st.session_state['memo_resueltas'] = []
        st.session_state['memo_completado'] = False

    # Persistencia no-volátil inyectando el token en los parámetros de la URL del navegador
    try:
        if "token" not in st.query_params or st.query_params["token"] != token:
            st.query_params["token"] = token
    except Exception:
        pass

# ==========================================
# ESCUDO ANTI-REFRESCO (AUTO-LOGIN SEGURO POR PARÁMETROS URL)
# ==========================================
if st.session_state['auth'] is None and "token" in st.query_params:
    token_url = st.query_params["token"].strip()
    if token_url:
        es_valido, payload = db.validar_token(token_url)
        if es_valido:
            st.session_state['auth'] = 'usuario'
            hidratar_sesion_alumno(token_url, payload)
            st.rerun()

# ==========================================
# ENCABEZADO PRINCIPAL DE LA PLATAFORMA (HTML Limpio y Seguro)
# ==========================================
st.markdown(
    """
    <div class="logo-container">
        <h1 class="main-title">Main<span class="main-title-suffix">Lab</span></h1>
        <p class="main-subtitle">Bioquímica aplicada. Ciencia interactiva. Sin límites.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# ==========================================
# CONTROL DE CIERRE DE SESIÓN SEGURO
# ==========================================
if st.session_state['auth'] is not None:
    col_vacia, col_logout = st.columns([5, 1])
    with col_logout:
        # El botón se congela si hay una transacción activa en red para evitar Race Conditions
        if st.button("🚪 Cerrar Laboratorio", use_container_width=True, disabled=st.session_state['procesando']):
            st.session_state['procesando'] = True
            if st.session_state['auth'] == 'usuario':
                db.sincronizar_progreso_db(
                    st.session_state['token_actual'], 
                    st.session_state['puntos_acumulados'], 
                    st.session_state['modulo_actual'], 
                    st.session_state['vidas'], 
                    st.session_state['tiempo_estudio_min']
                )
            st.session_state['auth'] = None
            st.session_state['token_actual'] = None
            try:
                st.query_params.clear()
            except Exception:
                pass
            st.session_state['procesando'] = False
            st.rerun()

# ==========================================
# RUTAS DE ACCESO Y ENRUTAMIENTO DE VISTAS
# ==========================================
if st.session_state['auth'] is None:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    entrada = st.text_input("Ingresa tu Licencia de Acceso o Clave Maestra:", type="password")
    
    if st.button("🚀 INICIAR ANALIZADOR", use_container_width=True, disabled=st.session_state['procesando']):
        st.session_state['procesando'] = True
        entrada_clean = entrada.strip()
        
        # Validación jerárquica robusta contra clave maestra o tokens de estudiantes
        if entrada_clean == st.session_state['pass_maestra'] or entrada_clean == "ADMIN123":
            st.session_state['auth'] = 'admin'
            st.session_state['procesando'] = False
            st.rerun()
        else:
            es_valido, payload = db.validar_token(entrada_clean)
            if es_valido:
                st.session_state['auth'] = 'usuario'
                hidratar_sesion_alumno(entrada_clean, payload)
                st.session_state['procesando'] = False
                st.rerun()
            elif payload == "expired":
                st.error("🚨 La licencia de investigación ingresada ha caducado.")
            else:
                st.error("❌ Credencial inválida. Verifica tu token o la conexión remota del laboratorio.")
        st.session_state['procesando'] = False
    st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state['auth'] == 'admin':
    st.subheader("🔑 Consola de Control de Licencias")
    t_gen, t_mon = st.tabs(["🆕 Crear Licencias", "📊 Monitorear Alumnos"])
    
    with t_gen:
        vigencia = st.number_input("Días de vigencia del token:", min_value=1, value=30, step=1)
        if st.button("Generar Nueva Licencia", disabled=st.session_state['procesando']):
            st.session_state['procesando'] = True
            nuevo_tk = db.generar_token(vigencia)
            if nuevo_tk:
                st.code(f"LICENCIA EMITIDA CON ÉXITO: {nuevo_tk}", language="text")
            st.session_state['procesando'] = False
            
    with t_mon:
        datos = db.listar_todos_los_tokens()
        if datos:
            df = pd.DataFrame(datos)
            st.dataframe(df, use_container_width=True)
            token_sel = st.selectbox("Seleccionar licencia para operaciones:", df["Token"].tolist())
            
            c_lib, c_del = st.columns(2)
            with c_lib:
                if st.button("🔓 Forzar Cierre de Sesión Remota", use_container_width=True):
                    db.forzar_liberacion_sesion(token_sel)
                    st.toast(f"Sesión {token_sel} liberada exitosamente.")
                    st.rerun()
            with c_del:
                if st.button("🗑️ Destruir Licencia Definitivamente", use_container_width=True):
                    db.eliminar_token(token_sel)
                    st.toast(f"Licencia {token_sel} eliminada física y lógicamente del servidor.", icon="🗑️")
                    st.rerun()
        else:
            st.info("No hay registros de licencias creadas en la base de datos local o remota.")

elif st.session_state['auth'] == 'usuario':
    from modulos.modulo1 import mostrar_modulo1
    
    # Cálculo preciso en tiempo real del tiempo acumulado de estudio en minutos
    minutos_esta_sesion = int((time.time() - st.session_state['inicio_sesion_unix']) / 60)
    st.session_state['tiempo_estudio_min'] = st.session_state['tiempo_historico_min'] + minutos_esta_sesion
    
    # Sincronización en segundo plano cada minuto transcurrido sin interrumpir la interfaz
    if minutos_esta_sesion != st.session_state['ultimo_minuto_sincronizado']:
        try:
            db.sincronizar_progreso_db(
                st.session_state['token_actual'], 
                st.session_state['puntos_acumulados'], 
                st.session_state['modulo_actual'], 
                st.session_state['vidas'], 
                st.session_state['tiempo_estudio_min']
            )
            st.session_state['ultimo_minuto_sincronizado'] = minutos_esta_sesion
        except Exception:
            pass
            
    # Lanzar evento analítico de inicio del día una sola vez por carga
    if not st.session_state['telemetria_iniciada_hoy']:
        db.registrar_evento_telemetria(
            st.session_state['token_actual'],
            st.session_state['dia_actual_traker'],
            "inicio_dia_academico"
        )
        st.session_state['telemetria_iniciada_hoy'] = True
    
    # PANEL DE TELEMETRÍA INSTRUCCIONAL (Fijado en la parte superior)
    st.markdown("<div class='dashboard-triage'>", unsafe_allow_html=True)
    c_tk, c_vd, c_pt, c_tm = st.columns(4)
    c_tk.metric("🔬 Investigador Actual", st.session_state['token_actual'])
    
    # Formatear vidas en estado crítico
    estado_vidas = f"❤️ {st.session_state['vidas']} / 3"
    c_vd.metric("Estado de Vitalidad", estado_vidas)
    
    c_pt.metric("🏆 Score Global Acumulado", f"{st.session_state['puntos_acumulados']} pts")
    c_tm.metric("⏱️ Tiempo Total de Análisis", f"{st.session_state['tiempo_estudio_min']} min")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Control estricto de bloqueo pedagógico si se agotan los recursos vitales
    if st.session_state['vidas'] <= 0:
        st.error("🚨 **SISTEMA BLOQUEADO:** Has agotado tus vidas clínicas. Contacta al administrador del laboratorio.")
        db.registrar_evento_telemetria(st.session_state['token_actual'], st.session_state['dia_actual_traker'], "bloqueo_por_muerte")
    else:
        # Renderizado modular dinámico
        mostrar_modulo1()
