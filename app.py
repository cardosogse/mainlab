import streamlit as st
import pandas as pd
import database as db
from assets import cargar_estilos, mezclar_memorama

st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
db.inicializar_db()

if 'auth' not in st.session_state: st.session_state['auth'] = None

pass_maestra_actual = db.obtener_password_admin()

# Cabecera con Layout Limpio y Botón de Desconexión
col_tit, col_logout = st.columns([4, 1])
with col_tit:
    st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)
with col_logout:
    if st.session_state['auth'] is not None:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        if st.button("Cerrar Sesión 🚪", use_container_width=True):
            st.session_state['auth'] = None
            st.rerun()

def hidratar_sesion_alumno(token, datos_db):
    st.session_state['token_actual'] = token
    st.session_state['puntos_acumulados'] = datos_db["puntos"]
    st.session_state['vidas'] = datos_db["vidas"]
    st.session_state['errores_quiz'] = datos_db["errores"]
    st.session_state['advertencia_ph'] = False
    st.session_state['memo_reveladas'] = []
    st.session_state['memo_resueltas'] = []
    st.session_state['racha_consecutiva'] = 0
    st.session_state['licencia_extendida'] = False
    st.session_state['memo_completado'] = False
    if 'memo_tablero' not in st.session_state or not st.session_state['memo_tablero']:
        st.session_state['memo_tablero'] = mezclar_memorama()

# Formulario de Acceso Unificado (CORREGIDO)
if st.session_state['auth'] is None or st.session_state['auth'] is False:
    entrada = st.text_input("Ingresa Token o Clave Maestra:", type="password")
    if st.button("🚀 ACCEDER AL LABORATORIO", use_container_width=True):
        if entrada == pass_maestra_actual:
            st.session_state['auth'] = 'admin'
            st.rerun()
        else:
            es_valido, payload = db.validar_token(entrada)
            if es_valido == True:
                st.session_state['auth'] = 'usuario'
                hidratar_sesion_alumno(entrada, payload)
                st.rerun()
            elif payload == "expired":
                st.error("🚨 El token ingresado ha caducado.")
            else:
                st.error("Credencial inválida.")

# --- CONSOLA DEL ADMINISTRADOR ---
if st.session_state['auth'] == 'admin':
    st.subheader("🔑 Consola de Gestión")
    t_gen, t_mon, t_diag = st.tabs(["🆕 Generar Tokens", "📊 Monitor de Alumnos", "🩺 Diagnóstico"])
    
    with t_gen:
        vigencia = st.number_input("Días de vigencia de la licencia:", min_value=1, value=30)
        if st.button("Emitir Nuevo Token"):
            nuevo_tk = db.generar_token(vigencia)
            st.code(f"TOKEN EMITIDO: {nuevo_tk}", language="text")
            
    with t_mon:
        datos = db.listar_todos_los_tokens()
        if datos:
            df = pd.DataFrame(datos)
            st.dataframe(df, use_container_width=True)
            
            token_sel = st.selectbox("Seleccionar Token de la Lista:", df["Token"].tolist())
            
            c_lib, c_del = st.columns(2)
            with c_lib:
                if st.button("🔓 Forzar Cierre de Sesión", use_container_width=True):
                    db.forzar_liberacion_sesion(token_sel)
                    st.toast(f"Sesión {token_sel} liberada.")
                    st.rerun()
            with c_del:
                if st.button("❌ Borrar Token Definitivamente", use_container_width=True):
                    db.eliminar_token(token_sel)
                    st.toast(f"Token {token_sel} eliminado con éxito de Supabase.", icon="🗑️")
                    st.rerun()
        else:
            st.info("No hay tokens ni alumnos registrados en el sistema.")
        
    with t_diag:
        if st.button("Ejecutar Auditoría de Enlace"):
            rep = db.verificar_salud_sistema()
            st.write(f"### Status: {rep['status']}")
            for d in rep["detalles"]: st.caption(f"- {d}")

# --- INTERFAZ DEL ALUMNO ---
elif st.session_state['auth'] == 'usuario':
    from modulos.modulo1 import mostrar_modulo1
    
    c_tk, c_vd, c_pt = st.columns(3)
    c_tk.metric("🔬 Investigador Actual", st.session_state['token_actual'])
    c_vd.metric("❤️ Vidas Críticas", f"{st.session_state['vidas']} / 3")
    c_pt.metric("🏆 Score Global", f"{st.session_state['puntos_acumulados']} pts")
    
    if st.session_state['vidas'] <= 0:
        st.error("🚨 **SISTEMA BLOQUEADO:** Has agotado tus vidas clínicas. Contacta al docente del laboratorio.")
    else:
        mostrar_modulo1()
