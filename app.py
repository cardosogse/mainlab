import streamlit as st
import pandas as pd
import database as db
from assets import cargar_estilos, mezclar_memorama

st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
db.inicializar_db()

if 'auth' not in st.session_state: st.session_state['auth'] = None

pass_maestra_actual = db.obtener_password_admin()
st.markdown("<h1 class='main-title'>Main<span class='main-title-suffix'>Lab</span></h1>", unsafe_allow_html=True)

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

if not st.session_state['auth']:
    entrada = st.text_input("Ingresa Token o Clave Maestra:", type="password")
    if st.button("🚀 ACCEDER AL LABORATORIO"):
        if entrada == pass_maestra_actual:
            st.session_state['auth'] = 'admin'
            st.rerun()
        else:
            es_valido, payload = db.validar_token(entrada)
            if es_valido:
                st.session_state['auth'] = 'usuario'
                hidratar_sesion_alumno(entrada, payload)
                st.rerun()
            else:
                st.error("Credencial inválida.")

if st.session_state['auth'] == 'admin':
    st.subheader("🔑 Consola de Gestión")
    t_gen, t_mon, t_diag = st.tabs(["🆕 Generar Tokens", "📊 Monitor de Alumnos", "🩺 Diagnóstico"])
    
    with t_gen:
        vigencia = st.number_input("Días de vigencia:", min_value=1, value=30)
        if st.button("Emitir Nuevo Token"):
            st.code(f"TOKEN EMITIDO: {db.generar_token(vigencia)}")
            
    with t_mon:
        datos = db.listar_todos_los_tokens()
        if datos:
            df = pd.DataFrame(datos)
            st.dataframe(df, use_container_width=True)
            token_sel = st.selectbox("Seleccionar Token del Alumno:", df["Token"].tolist())
            if st.button("🔓 Desbloquear Sesión (Forzar Cierre)"):
                db.forzar_liberacion_sesion(token_sel)
                st.success(f"Sesión {token_sel} liberada.")
                st.rerun()
        else: st.info("No hay alumnos registrados.")
        
    with t_diag:
        if st.button("Ejecutar Auditoría de Enlace"):
            rep = db.verificar_salud_sistema()
            st.write(f"### Status: {rep['status']}")
            for d in rep["detalles"]: st.caption(f"- {d}")

elif st.session_state['auth'] == 'usuario':
    from modulos.modulo1 import mostrar_modulo1
    
    # Barra de estado superior interactiva
    c_tk, c_vd, c_pt = st.columns(3)
    c_tk.metric("🔬 Investigador Actual", st.session_state['token_actual'])
    c_vd.metric("❤️ Vidas Críticas", f"{st.session_state['vidas']} / 3")
    c_pt.metric("🏆 Score Global", f"{st.session_state['puntos_acumulados']} pts")
    
    if st.session_state['vidas'] <= 0:
        st.error("🚨 **SISTEMA BLOQUEADO:** Has agotado tus vidas clínicas. Contacta al administrador del laboratorio.")
    else:
        mostrar_modulo1()
