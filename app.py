import streamlit as st
import pandas as pd
import database as db
from assets import cargar_estilos

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
db.inicializar_db()

# --- PANEL ADMINISTRADOR ---
def panel_administrador():
    st.subheader("🔑 Consola de Gestión")
    t1, t2, t3, t4 = st.tabs(["🆕 Tokens", "📊 Monitor", "⚙️ Seguridad", "🩺 Diagnóstico"])
    with t1:
        if st.button("Emitir Token"): st.code(db.generar_token(30))
    with t2:
        datos = db.listar_todos_los_tokens()
        st.dataframe(pd.DataFrame(datos))
        t_sel = st.selectbox("Token:", [d['token'] for d in datos])
        if st.button("🚫 Eliminar"): db.eliminar_token(t_sel); st.rerun()
        if st.button("🔓 Forzar Cierre"): db.forzar_liberacion_sesion(t_sel); st.rerun()
    with t3:
        if st.button("Actualizar Clave"): db.actualizar_password_admin(st.text_input("Nueva:", type="password"))
    with t4:
        if st.button("Reparar"): st.success(db.limpiar_inconsistencias_db()); st.rerun()

# --- FLUJO PRINCIPAL ---
st.markdown("<h1 class='main-title'>MainLab</h1>", unsafe_allow_html=True)

entrada = st.text_input("Ingresa Token o Clave:", type="password")

if st.button("🚀 ACCEDER"):
    if entrada == db.obtener_password_admin():
        st.session_state['auth'] = 'admin'
        st.rerun()
    elif db.validar_token(entrada)[0]:
        st.session_state['auth'] = entrada
        st.rerun()

if st.session_state.get('auth') == 'admin':
    panel_administrador()
elif st.session_state.get('auth'):
    # Importación DIFERIDA (evita el bucle de errores)
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
    
    estacion = st.radio("Día:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
    if estacion == "Día 1": mostrar_dia1()
    elif estacion == "Día 2": mostrar_dia2()
    elif estacion == "Día 3": mostrar_dia3()
    else: mostrar_dia4()
