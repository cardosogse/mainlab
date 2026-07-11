import streamlit as st
import pandas as pd
import time
import database as db
from assets import cargar_estilos

st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬", initial_sidebar_state="expanded")

cargar_estilos()
db.inicializar_db()

def inicializar_estados_globales():
    variables = {
        'auth': None, 'token_actual': None, 'procesando': False,
        'puntos_acumulados': 0, 'vidas': 3, 'tiempo_historico_min': 0,
        'tiempo_estudio_min': 0, 'inicio_sesion_unix': None, 'modulo_actual': "1"
    }
    for k, v in variables.items():
        if k not in st.session_state: st.session_state[k] = v

inicializar_estados_globales()
pass_maestra = db.obtener_password_admin()

# --- ESCUDO ANTI-REFRESCO BLINDADO CONTRA ERRORES 'OH NO.' ---
if st.session_state['auth'] is None and "token" in st.query_params:
    token_url = st.query_params["token"].strip()
    if token_url and len(token_url) > 0:
        es_valido, payload = db.validar_token(token_url)
        if es_valido:
            st.session_state['auth'] = 'usuario'
            st.session_state['token_actual'] = token_url
            st.session_state['puntos_acumulados'] = payload.get("puntos", 0)
            st.session_state['vidas'] = payload.get("vidas", 3)
            st.session_state['tiempo_historico_min'] = payload.get("tiempo", 0)
            st.session_state['inicio_sesion_unix'] = time.time()
            st.rerun()
        else:
            st.query_params.clear()
            st.rerun()

# --- CABECERA ESTÉTICA COMPLETA SISTEMA 1 ---
st.markdown(
    """
    <div class="logo-container">
        <h1 class="main-title">Main<span class="main-title-suffix">Lab</span></h1>
        <p class="main-subtitle">Bioquimica aplicada. Ciencia interactiva. Sin limites.</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- PANEL DE LOGIN SEGURO ---
if st.session_state['auth'] is None:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    entrada = st.text_input("Ingresa Licencia o Clave Maestra:", type="password")
    
    if st.button("🚀 ACCEDER AL LABORATORIO", use_container_width=True):
        entrada_clean = entrada.strip()
        if pass_maestra and entrada_clean == pass_maestra:
            st.session_state['auth'] = 'admin'
            st.rerun()
        else:
            es_valido, payload = db.validar_token(entrada_clean)
            if es_valido:
                st.session_state['auth'] = 'usuario'
                st.session_state['token_actual'] = entrada_clean
                st.session_state['puntos_acumulados'] = payload["puntos"]
                st.session_state['vidas'] = payload["vidas"]
                st.session_state['tiempo_historico_min'] = payload["tiempo"]
                st.session_state['inicio_sesion_unix'] = time.time()
                st.query_params["token"] = entrada_clean
                st.rerun()
            elif payload == "expired":
                st.error("🚨 Esta licencia de investigación ha caducado.")
            else:
                st.error("❌ Credencial inválida.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- CONSOLA DE ADMINISTRACIÓN EXPANDIDA ---
elif st.session_state['auth'] == 'admin':
    st.subheader("🔑 Consola de Licencias")
    t_gen, t_mon = st.tabs(["🆕 Crear Licencias", "📊 Monitorear Alumnos"])
    
    with t_gen:
        vigencia = st.number_input("Días de vigencia:", min_value=1, value=30)
        if st.button("Generar Nueva Licencia"):
            nuevo_tk = db.generar_token(vigencia)
            if nuevo_tk: st.code(f"TOKEN: {nuevo_tk}", language="text")
            
    with t_mon:
        datos = db.listar_todos_los_tokens()
        if datos:
            df = pd.DataFrame(datos)
            st.dataframe(df, use_container_width=True)
            
            # --- SECCIÓN DE ELIMINACIÓN DE TOKENS HABILITADA ---
            st.markdown("---")
            st.markdown("#### 🗑️ Zona de Revocación de Licencias")
            token_sel = st.selectbox("Selecciona un Token de la matriz para eliminarlo:", df["Token"].tolist())
            if st.button("❌ DESTRUIR LICENCIA DEFINITIVAMENTE", use_container_width=True):
                db.eliminar_token(token_sel)
                st.toast(f"Licencia {token_sel} purgada con éxito.", icon="🗑️")
                time.sleep(1.0)
                st.rerun()
        else:
            st.info("No hay registros en la base de datos.")
        
    if st.button("🚪 Salir de Panel"):
        st.session_state['auth'] = None
        st.rerun()

elif st.session_state['auth'] == 'usuario':
    minutos_sesion = int((time.time() - st.session_state['inicio_sesion_unix']) / 60)
    st.session_state['tiempo_estudio_min'] = st.session_state['tiempo_historico_min'] + minutos_sesion
    
    st.markdown("<div class='dashboard-triage'>", unsafe_allow_html=True)
    c_tk, c_vd, c_pt, c_tm = st.columns(4)
    c_tk.metric("🔬 Licencia", st.session_state['token_actual'])
    c_vd.metric("❤️ Vitalidad", f"{st.session_state['vidas']} / 3")
    c_pt.metric("🏆 Score", f"{st.session_state['puntos_acumulados']} pts")
    c_tm.metric("⏱️ Tiempo", f"{st.session_state['tiempo_estudio_min']} min")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.session_state['vidas'] <= 0:
        st.error("🚨 **SISTEMA BLOQUEADO:** Has agotado tus vidas clínicas. Contacta al docente.")
    else:
        from modulos.modulo1 import app as ejecutar_modulo1
        ejecutar_modulo1()
