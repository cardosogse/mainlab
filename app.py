import streamlit as st
import pandas as pd
import time
import database as db
from assets import cargar_estilos, mezclar_memorama

st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
db.inicializar_db()

if 'auth' not in st.session_state: st.session_state['auth'] = None

pass_maestra_actual = db.obtener_password_admin()

# Cabecera Global con logotipo simétrico y centrado
st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)

if st.session_state['auth'] is not None:
    _, col_logout = st.columns([4, 1])
    with col_logout:
        if st.button("Cerrar Sesión 🚪", use_container_width=True):
            if st.session_state['auth'] == 'usuario':
                db.sincronizar_progreso_db(
                    st.session_state['token_actual'], 
                    st.session_state['puntos_acumulados'], 
                    "1", 
                    st.session_state['vidas'], 
                    st.session_state['tiempo_estudio_min']
                )
            st.session_state['auth'] = None
            st.rerun()

def hidratar_sesion_alumno(token, datos_db):
    st.session_state['token_actual'] = token
    st.session_state['puntos_acumulados'] = datos_db["puntos"]
    st.session_state['vidas'] = datos_db["vidas"]
    st.session_state['errores_quiz'] = datos_db["errores"]
    # MODIFICADO: Hidratación con almacenamiento de minutos históricos
    st.session_state['tiempo_historico_min'] = datos_db["tiempo"]
    st.session_state['tiempo_estudio_min'] = datos_db["tiempo"]
    st.session_state['inicio_sesion_unix'] = time.time()
    st.session_state['advertencia_ph'] = False
    st.session_state['memo_reveladas'] = []
    st.session_state['memo_resueltas'] = []
    st.session_state['racha_consecutiva'] = 0
    st.session_state['licencia_extendida'] = False
    st.session_state['memo_completado'] = False
    if 'memo_tablero' not in st.session_state or not st.session_state['memo_tablero']:
        st.session_state['memo_tablero'] = mezclar_memorama()

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

if st.session_state['auth'] == 'admin':
    st.subheader("🔑 Consola de Gestión")
    t_gen, t_mon = st.tabs(["🆕 Generar Tokens", "📊 Monitor de Alumnos"])
    
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
                    st.toast(f"Token {token_sel} eliminado con éxito.", icon="🗑️")
                    st.rerun()
        else: st.info("No hay tokens registrados.")

elif st.session_state['auth'] == 'usuario':
    from modulos.modulo1 import mostrar_modulo1
    
    # MODIFICADO: Telemetría síncrona pasiva en base a minutos transcurridos
    minutos_esta_sesion = int((time.time() - st.session_state['inicio_sesion_unix']) / 60)
    st.session_state['tiempo_estudio_min'] = st.session_state['tiempo_historico_min'] + minutos_esta_sesion
    
    try:
        db.sincronizar_progreso_db(
            st.session_state['token_actual'], 
            st.session_state['puntos_acumulados'], 
            "1", 
            st.session_state['vidas'], 
            st.session_state['tiempo_estudio_min']
        )
    except:
        pass
    
    # Renderizado estático estable de métricas
    c_tk, c_vd, c_pt, c_tm = st.columns(4)
    c_tk.metric("🔬 Investigador Actual", st.session_state['token_actual'])
    c_vd.metric("❤️ Vidas Críticas", f"{st.session_state['vidas']} / 3")
    c_pt.metric("🏆 Score Global", f"{st.session_state['puntos_acumulados']} pts")
    c_tm.metric("⏱️ Tiempo de Estudio", f"{st.session_state['tiempo_estudio_min']} min")
    
    if st.session_state['vidas'] <= 0:
        st.error("🚨 **SISTEMA BLOQUEADO:** Has agotado tus vidas clínicas.")
    else:
        mostrar_modulo1()
