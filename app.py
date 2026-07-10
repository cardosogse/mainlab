import streamlit as st
import pandas as pd
import database as db
from assets import cargar_estilos

# 1. Configuración
st.set_page_config(page_title="MainLab", layout="wide", page_icon="🧬")
cargar_estilos()
db.inicializar_db()

# 2. Carga de módulos (Importación diferida para evitar bucles)
def obtener_modulos():
    from modulos.m1_dia1 import mostrar_dia1
    from modulos.m1_dia2 import mostrar_dia2
    from modulos.m1_dia3 import mostrar_dia3
    from modulos.m1_dia4 import mostrar_dia4
    return mostrar_dia1, mostrar_dia2, mostrar_dia3, mostrar_dia4

# 3. Flujo Principal
st.markdown("<h1 class='main-title'>MainLab</h1>", unsafe_allow_html=True)

if 'auth' not in st.session_state: st.session_state['auth'] = None

entrada = st.text_input("Ingresa credencial:", type="password")

if st.button("🚀 ACCEDER AL LABORATORIO"):
    if entrada == db.obtener_password_admin():
        st.session_state['auth'] = 'admin'
        st.rerun()
    elif db.validar_token(entrada)[0]:
        st.session_state['auth'] = entrada
        st.rerun()
    else: st.error("Credencial inválida")

if st.session_state['auth'] == 'admin':
    st.subheader("🔑 Consola de Gestión")
    t1, t2, t3, t4 = st.tabs(["🆕 Tokens", "📊 Monitor", "⚙️ Seguridad", "🩺 Diagnóstico"])
    with t1:
        if st.button("Emitir Token"): st.code(db.generar_token(30))
    with t2:
        st.dataframe(pd.DataFrame(db.listar_todos_los_tokens(), columns=["Token", "Uso", "Exp", "Pts", "Vidas", "Mod"]))
        t_sel = st.selectbox("Token:", [d[0] for d in db.listar_todos_los_tokens()])
        c1, c2 = st.columns(2)
        if c1.button("🚫 Eliminar"): db.eliminar_token(t_sel); st.rerun()
        if c2.button("🔓 Liberar"): db.liberar_token(t_sel); st.rerun()
    with t3:
        if st.button("Guardar"): db.actualizar_password_admin(st.text_input("Nueva:", type="password"))
    with t4:
        if st.button("🛠️ Reparar"): st.success(db.limpiar_inconsistencias_db()); st.rerun()

elif st.session_state['auth']:
    m1, m2, m3, m4 = obtener_modulos()
    estacion = st.radio("Día:", ["Día 1", "Día 2", "Día 3", "Día 4"], horizontal=True)
    if estacion == "Día 1": m1()
    elif estacion == "Día 2": m2()
    elif estacion == "Día 3": m3()
    else: m4()
